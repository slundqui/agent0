"""Script for fuzzing profit values on immediately opening & closing a long or short.


# Test procedure
- spin up local chain, deploy hyperdrive with fees
- open a long for a random amount
- advance time, but not enough to trigger a new checkpoint
- close the long
- open a short for a random amount
- advance time, but not enough to trigger a new checkpoint
- close the short
- invariance checks

# Invariance checks (these should be True):
# We are checking that the agent made made no profit
- Repeat these two checks for the longs & shorts
  - transaction receipt: base amount returned < base amount provided
  - agent wallet: final balance <= initial balance
- Specific values checked
  - trade amount
  - agent initial balance
  - agent final balance
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from typing import Any, NamedTuple, Sequence

import numpy as np
from fixedpointmath import FixedPoint

from agent0.core.hyperdrive.crash_report import build_crash_trade_result, log_hyperdrive_crash_report
from agent0.core.hyperdrive.interactive import LocalChain
from agent0.hyperfuzz import FuzzAssertionException

from .helpers import advance_time_after_checkpoint, advance_time_before_checkpoint, setup_fuzz

# pylint: disable=too-many-locals


def main(argv: Sequence[str] | None = None):
    """Primary entrypoint.

    Arguments
    ---------
    argv: Sequence[str]
        The argv values returned from argparser.
    """
    parsed_args = parse_arguments(argv)
    fuzz_profit_check(*parsed_args)


def fuzz_profit_check(chain_config: LocalChain.Config, steth: bool = False, pause_on_fail: bool = False):
    """Fuzzes invariant checks for profit from long and short positions.

    Parameters
    ----------
    chain_config: LocalChain.Config, optional
        Configuration options for the local chain.
    steth: bool
        Whether to use steth instead of erc4626
    pause_on_fail: bool
        If True, pause on test failure.
    """
    # pylint: disable=too-many-statements

    # Setup the environment
    chain, random_seed, rng, hyperdrive_pool = setup_fuzz(
        chain_config,
        fuzz_test_name="fuzz_profit_check",
        flat_fee=FixedPoint(0),
        curve_fee=FixedPoint(0.001),  # 0.1%
        governance_lp_fee=FixedPoint(0),
        governance_zombie_fee=FixedPoint(0),
        var_interest=FixedPoint(0.0),
        steth=steth,
    )

    # Get a random trade amount
    long_trade_amount = FixedPoint(
        scaled_value=int(
            np.floor(
                rng.uniform(
                    low=hyperdrive_pool.interface.pool_config.minimum_transaction_amount.scaled_value,
                    high=hyperdrive_pool.interface.calc_max_long(
                        FixedPoint(1e9), hyperdrive_pool.interface.current_pool_state
                    ).scaled_value,
                )
            )
        )
    )

    # Generate funded trading agent
    long_agent = chain.init_agent(base=long_trade_amount, eth=FixedPoint(100), pool=hyperdrive_pool, name="alice")
    long_agent_initial_balance = long_agent.get_wallet().balance.amount

    # Advance time to be right after a checkpoint boundary
    logging.info("Advance time...")
    advance_time_after_checkpoint(chain, hyperdrive_pool)

    # Open a long
    logging.info("Open a long...")
    open_long_event = long_agent.open_long(base=long_trade_amount)

    starting_checkpoint_id = hyperdrive_pool.interface.calc_checkpoint_id()

    # Let some time pass, as long as it is less than a checkpoint
    # This means that the open & close will get pro-rated to the same spot
    logging.info("Advance time...")
    advance_time_before_checkpoint(chain, rng, hyperdrive_pool)

    # Close the long
    logging.info("Close the long...")
    close_long_event = long_agent.close_long(
        maturity_time=open_long_event.args.maturity_time, bonds=open_long_event.args.bond_amount
    )
    ending_checkpoint_id = hyperdrive_pool.interface.calc_checkpoint_id()

    # Ensure open + close are within same checkpoint
    assert starting_checkpoint_id == ending_checkpoint_id

    # Open a short
    short_trade_amount = FixedPoint(
        scaled_value=int(
            np.floor(
                rng.uniform(
                    low=hyperdrive_pool.interface.pool_config.minimum_transaction_amount.scaled_value,
                    high=hyperdrive_pool.interface.calc_max_short(
                        FixedPoint(1e9), hyperdrive_pool.interface.current_pool_state
                    ).scaled_value,
                )
            )
        )
    )
    # Generate funded trading agent
    # the short trade amount is in bonds, but we know we will need much less base
    # we can play it safe by initializing with that much base
    short_agent = chain.init_agent(base=short_trade_amount, eth=FixedPoint(100), pool=hyperdrive_pool, name="bob")
    short_agent_initial_balance = short_agent.get_wallet().balance.amount

    # Advance time to be right after a checkpoint boundary
    logging.info("Advance time...")
    advance_time_after_checkpoint(chain, hyperdrive_pool)

    # Set trade amount to the new wallet position (due to losing money from the previous open/close)
    logging.info("Open a short...")
    open_short_event = short_agent.open_short(bonds=short_trade_amount)
    starting_checkpoint_id = hyperdrive_pool.interface.calc_checkpoint_id()

    # Let some time pass, as long as it is less than a checkpoint
    # This means that the open & close will get pro-rated to the same spot
    logging.info("Advance time...")
    advance_time_before_checkpoint(chain, rng, hyperdrive_pool)

    # Close the short
    logging.info("Close the short...")
    close_short_event = short_agent.close_short(
        maturity_time=open_short_event.args.maturity_time, bonds=open_short_event.args.bond_amount
    )
    ending_checkpoint_id = hyperdrive_pool.interface.calc_checkpoint_id()

    # Ensure open + close are within same checkpoint
    assert starting_checkpoint_id == ending_checkpoint_id

    logging.info("Check invariants...")
    # Ensure that the prior trades did not result in a profit
    check_data = {
        "long_trade_amount": long_trade_amount,
        "long_agent_initial_balance": long_agent_initial_balance,
        "long_agent_final_balance": long_agent.get_wallet().balance.amount,
        "long_events": {"open": open_long_event, "close": close_long_event},
        "short_trade_amount": short_trade_amount,
        "short_agent_final_balance": short_agent.get_wallet().balance.amount,
        "short_agent_initial_balance": short_agent_initial_balance,
        "short_events": {"open": open_short_event, "close": close_short_event},
    }
    try:
        invariant_check(check_data)
    except FuzzAssertionException as error:
        dump_state_dir = chain.save_state(save_prefix="fuzz_profit_check")

        # The additional information going into the crash report
        additional_info = {
            "fuzz_random_seed": random_seed,
            "dump_state_dir": dump_state_dir,
            "trade_events": hyperdrive_pool.get_trade_events(),
        }
        additional_info.update(error.exception_data)

        # The subset of information going into rollbar
        rollbar_data = {
            "fuzz_random_seed": random_seed,
            "dump_state_dir": dump_state_dir,
        }
        rollbar_data.update(error.exception_data)

        # TODO do better checking here or make agent optional in build_crash_trade_result
        if "LONG" in error.args[0]:
            account = long_agent.account
        else:
            account = short_agent.account
        report = build_crash_trade_result(error, hyperdrive_pool.interface, account, additional_info=additional_info)
        # Crash reporting already going to file in logging
        log_hyperdrive_crash_report(
            report,
            crash_report_to_file=True,
            crash_report_stdout_summary=False,
            crash_report_file_prefix="fuzz_profit_check",
            log_to_rollbar=True,
            rollbar_log_level_threshold=chain.config.rollbar_log_level_threshold,
            rollbar_log_filter_func=chain_config.rollbar_log_filter_func,
            rollbar_data=rollbar_data,
        )
        if pause_on_fail:
            # We don't log info from logging, so we print to ensure this shows up
            print(
                f"Pausing pool (pool:{hyperdrive_pool.hyperdrive_address} port:{chain_config.chain_port}) "
                f"crash {repr(error)}"
            )
            while True:
                time.sleep(1000000)

        chain.cleanup()
        raise error
    chain.cleanup()
    logging.info("Test passed!")


class Args(NamedTuple):
    """Command line arguments for the invariant checker."""

    chain_config: LocalChain.Config


def namespace_to_args(namespace: argparse.Namespace) -> Args:
    """Converts argprase.Namespace to Args.

    Arguments
    ---------
    namespace: argparse.Namespace
        Object for storing arg attributes.

    Returns
    -------
    Args
        Formatted arguments
    """
    return Args(
        chain_config=LocalChain.Config(chain_port=namespace.chain_port, log_to_stdout=namespace.log_to_stdout),
    )


def parse_arguments(argv: Sequence[str] | None = None) -> Args:
    """Parses input arguments.

    Arguments
    ---------
    argv: Sequence[str]
        The argv values returned from argparser.

    Returns
    -------
    Args
        Formatted arguments
    """
    parser = argparse.ArgumentParser(description="Runs a loop to check Hyperdrive invariants at each block.")
    parser.add_argument(
        "--chain_port",
        type=int,
        default=10000,
        help="The number of random trades to open.",
    )
    parser.add_argument(
        "--log_to_stdout",
        type=bool,
        default=False,
        help="If True, log to stdout in addition to a file.",
    )
    # Use system arguments if none were passed
    if argv is None:
        argv = sys.argv
    return namespace_to_args(parser.parse_args())


def invariant_check(check_data: dict[str, Any]) -> None:
    """Check the pool state invariants.

    Arguments
    ---------
    check_data: dict[str, Any]
        The trade data to check.
    """
    # pylint: disable=too-many-statements

    failed = False
    exception_message: list[str] = ["Fuzz Profit Check Invariant Check"]
    exception_data: dict[str, Any] = {}

    # Check long trade
    base_amount_returned: FixedPoint = check_data["long_events"]["close"].args.amount
    base_amount_provided: FixedPoint = check_data["long_events"]["open"].args.amount
    if base_amount_returned >= base_amount_provided:
        difference_in_wei = abs(base_amount_returned.scaled_value - base_amount_provided.scaled_value)
        exception_message.append("LONG: Amount returned on closing was too large.")
        exception_message.append(
            f"{base_amount_returned=} should not be >= {base_amount_provided=}. {difference_in_wei=}"
        )
        exception_data["invariance_check:long_base_amount_returned"] = base_amount_returned
        exception_data["invariance_check:long_base_amount_provided"] = base_amount_provided
        exception_data["invariance_check:long_base_amount_difference_in_wei"] = difference_in_wei
        failed = True

    initial_agent_balance: FixedPoint = check_data["long_agent_initial_balance"]
    final_agent_balance: FixedPoint = check_data["long_agent_final_balance"]
    if final_agent_balance > initial_agent_balance:
        difference_in_wei = abs(final_agent_balance.scaled_value - initial_agent_balance.scaled_value)
        exception_message.append("LONG: Agent made a profit when the should not have.")
        exception_message.append(
            f"{final_agent_balance=} should not be > {initial_agent_balance=}. {difference_in_wei=}"
        )
        exception_data["invariance_check:long_agent_initial_balance"] = initial_agent_balance
        exception_data["invariance_check:long_agent_final_balance"] = final_agent_balance
        exception_data["invariance_check:long_agent_balance_difference_in_wei"] = difference_in_wei
        failed = True

    # Check short trade
    base_amount_returned: FixedPoint = check_data["short_events"]["close"].args.amount
    base_amount_provided: FixedPoint = check_data["short_events"]["open"].args.amount
    if base_amount_returned >= base_amount_provided:
        difference_in_wei = abs(base_amount_returned.scaled_value - base_amount_provided.scaled_value)
        exception_message.append("SHORT: Amount returned on closing was too large.")
        exception_message.append(
            f"{base_amount_returned=} should not be >= {base_amount_provided=}. {difference_in_wei=}"
        )
        exception_data["invariance_check:short_base_amount_returned"] = base_amount_returned
        exception_data["invariance_check:short_base_amount_provided"] = base_amount_provided
        exception_data["invariance_check:short_base_amount_difference_in_wei"] = difference_in_wei
        failed = True

    initial_agent_balance: FixedPoint = check_data["short_agent_initial_balance"]
    final_agent_balance: FixedPoint = check_data["short_agent_final_balance"]
    if final_agent_balance > initial_agent_balance:
        difference_in_wei = abs(initial_agent_balance.scaled_value - final_agent_balance.scaled_value)
        exception_message.append("SHORT: Agent made a profit when the should not have.")
        exception_message.append(
            f"{final_agent_balance=} should not be > {initial_agent_balance=}. {difference_in_wei=}"
        )
        exception_data["invariance_check:short_agent_initial_balance"] = initial_agent_balance
        exception_data["invariance_check:short_agent_final_balance"] = final_agent_balance
        exception_data["invariance_check:short_agent_balance_difference_in_wei"] = difference_in_wei
        failed = True

    if failed:
        logging.critical("\n".join(exception_message))
        raise FuzzAssertionException(*exception_message, exception_data=exception_data)


if __name__ == "__main__":
    main()
