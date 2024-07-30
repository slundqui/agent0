"""Runs random bots on a mainnet fork to test yield sources."""

from __future__ import annotations

import argparse
import logging
import random
import sys
import time
from typing import NamedTuple, Sequence

import numpy as np
from web3.exceptions import ContractCustomError

from agent0 import LocalChain
from agent0.ethpy.base.errors import ContractCallException, UnknownBlockError
from agent0.hyperfuzz import FuzzAssertionException
from agent0.hyperfuzz.hyperdrive_fork_instances import StethHyperdrive
from agent0.hyperfuzz.system_fuzz import generate_fuzz_hyperdrive_config, run_fuzz_bots
from agent0.hyperlogs.rollbar_utilities import initialize_rollbar, log_rollbar_exception


def _fuzz_ignore_logging_to_rollbar(exc: Exception) -> bool:
    """Function defining errors to not log to rollbar during fuzzing.

    These are the two most common errors we see in local fuzz testing. These are
    known issues due to random bots not accounting for these cases, so we don't log them to
    rollbar.
    """
    if isinstance(exc, ContractCallException):
        orig_exception = exc.orig_exception
        if orig_exception is None:
            return False

        # Insufficient liquidity error
        if (
            isinstance(orig_exception, ContractCustomError)
            and len(orig_exception.args) > 1
            and "InsufficientLiquidity raised" in orig_exception.args[1]
        ):
            return True

        # Circuit breaker triggered error
        if (
            isinstance(orig_exception, ContractCustomError)
            and len(orig_exception.args) > 1
            and "CircuitBreakerTriggered raised" in orig_exception.args[1]
        ):
            return True

    return False


def _fuzz_ignore_errors(exc: Exception) -> bool:
    """Function defining errors to ignore for pausing chain during fuzzing."""
    # pylint: disable=too-many-return-statements
    # Ignored fuzz exceptions
    if isinstance(exc, FuzzAssertionException):
        # LP rate invariance check
        if (
            len(exc.args) >= 2
            and exc.args[0] == "Continuous Fuzz Bots Invariant Checks"
            and "lp_rate=" in exc.args[1]
            and "is expected to be >= vault_rate=" in exc.args[1]
        ):
            return True

    # Contract call exceptions
    elif isinstance(exc, ContractCallException):
        orig_exception = exc.orig_exception
        if orig_exception is None:
            return False

        # Insufficient liquidity error
        if (
            isinstance(orig_exception, ContractCustomError)
            and len(orig_exception.args) > 1
            and "InsufficientLiquidity raised" in orig_exception.args[1]
        ):
            return True

        # Circuit breaker triggered error
        if (
            isinstance(orig_exception, ContractCustomError)
            and len(orig_exception.args) > 1
            and "CircuitBreakerTriggered raised" in orig_exception.args[1]
        ):
            return True

        # DistributeExcessIdle error
        if (
            isinstance(orig_exception, ContractCustomError)
            and len(orig_exception.args) > 1
            and "DistributeExcessIdleFailed raised" in orig_exception.args[1]
        ):
            return True

        # DecreasedPresentValueWhenAddingLiquidity error
        if (
            isinstance(orig_exception, ContractCustomError)
            and len(orig_exception.args) > 1
            and "DecreasedPresentValueWhenAddingLiquidity raised" in orig_exception.args[1]
        ):
            return True

        # Status == 0
        if (
            # Lots of conditions to check
            # pylint: disable=too-many-boolean-expressions
            isinstance(orig_exception, list)
            and len(orig_exception) > 1
            and isinstance(orig_exception[0], UnknownBlockError)
            and len(orig_exception[0].args) > 0
            and "Receipt has status of 0" in orig_exception[0].args[0]
        ):
            return True

    return False


def main(argv: Sequence[str] | None = None) -> None:
    """Runs local fuzz bots.

    Arguments
    ---------
    argv: Sequence[str]
        A sequence containing the uri to the database server.
    """
    # TODO consolidate setup into single function and clean up.
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    parsed_args = parse_arguments(argv)

    log_to_rollbar = initialize_rollbar("forked_localfuzzbots")

    # Negative rng_seed means default
    if parsed_args.rng_seed < 0:
        rng_seed = random.randint(0, 10000000)
    else:
        rng_seed = parsed_args.rng_seed
    rng = np.random.default_rng(rng_seed)

    if parsed_args.rpc_uri == "":
        raise ValueError("rpc_uri must be set.")

    fork_block = None
    if parsed_args.fork_block != -1:
        fork_block = parsed_args.fork_block

    # Empty string means default
    if parsed_args.chain_host == "":
        chain_host = None
    else:
        chain_host = parsed_args.chain_host

    # Negative chain port means default
    if parsed_args.chain_port < 0:
        if parsed_args.lp_share_price_test:
            chain_port = 1111
        elif not parsed_args.lp_share_price_test:
            chain_port = 3333
        else:
            assert False
    else:
        chain_port = parsed_args.chain_port

    # Set different ports if we're doing lp share price test
    if parsed_args.lp_share_price_test:
        db_port = 5555
    elif not parsed_args.lp_share_price_test:
        db_port = 7777
    else:
        assert False

    local_chain_config = LocalChain.Config(
        chain_host=chain_host,
        chain_port=chain_port,
        db_port=db_port,
        block_timestamp_interval=12,
        log_level_threshold=logging.WARNING,
        preview_before_trade=True,
        log_to_rollbar=log_to_rollbar,
        rollbar_log_prefix="localfuzzbots",
        rollbar_log_filter_func=_fuzz_ignore_logging_to_rollbar,
        rng=rng,
        crash_log_level=logging.ERROR,
        rollbar_log_level_threshold=logging.ERROR,  # Only log errors and above to rollbar
        crash_report_additional_info={"rng_seed": rng_seed},
        gas_limit=int(1e6),  # Plenty of gas limit for transactions
        advance_time_create_checkpoint_retry_count=5,  # Try 5 times when creating checkpoints for advancing time
    )

    while True:
        # Build interactive local hyperdrive
        # TODO can likely reuse some of these resources
        # instead, we start from scratch every time.
        chain = LocalChain(fork_uri=parsed_args.rpc_uri, fork_block_number=fork_block, config=local_chain_config)

        # Fuzz over config values
        hyperdrive_config = generate_fuzz_hyperdrive_config(
            rng,
            lp_share_price_test=parsed_args.lp_share_price_test,
            steth=True,
        )

        hyperdrive_pool = StethHyperdrive(chain, hyperdrive_config)
        # try:
        #    hyperdrive_pool = StethHyperdrive(chain, hyperdrive_config)
        # except Exception as e:  # pylint: disable=broad-except
        #    logging.error(
        #        "Error deploying hyperdrive: %s",
        #        repr(e),
        #    )
        #    log_rollbar_exception(
        #        e,
        #        log_level=logging.ERROR,
        #        rollbar_log_prefix="Error deploying hyperdrive poolError deploying hyperdrive pool",
        #    )
        #    chain.cleanup()
        #    continue

        raise_error_on_fail = False
        if parsed_args.pause_on_invariance_fail:
            raise_error_on_fail = True

        # TODO submit multiple transactions per block
        try:
            run_fuzz_bots(
                chain,
                hyperdrive_pool,
                check_invariance=True,
                raise_error_on_failed_invariance_checks=raise_error_on_fail,
                raise_error_on_crash=raise_error_on_fail,
                log_to_rollbar=log_to_rollbar,
                ignore_raise_error_func=_fuzz_ignore_errors,
                run_async=False,
                random_advance_time=True,
                random_variable_rate=True,
                num_iterations=3000,
                lp_share_price_test=parsed_args.lp_share_price_test,
            )

        except Exception as e:  # pylint: disable=broad-except
            logging.error(
                "Pausing pool (pool:%s port:%s) on crash %s",
                hyperdrive_pool.hyperdrive_address,
                local_chain_config.chain_port,
                repr(e),
            )
            while True:
                time.sleep(1000000)

        chain.cleanup()


class Args(NamedTuple):
    """Command line arguments for the invariant checker."""

    lp_share_price_test: bool
    pause_on_invariance_fail: bool
    chain_host: str
    chain_port: int
    rng_seed: int
    rpc_uri: str
    fork_block: int


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
        lp_share_price_test=namespace.lp_share_price_test,
        pause_on_invariance_fail=namespace.pause_on_invariance_fail,
        chain_host=namespace.chain_host,
        chain_port=namespace.chain_port,
        rng_seed=namespace.rng_seed,
        rpc_uri=namespace.rpc_uri,
        fork_block=namespace.fork_block,
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
        "--lp-share-price-test",
        default=False,
        action="store_true",
        help="Runs the lp share price fuzz with specific fee and rate parameters.",
    )
    parser.add_argument(
        "--pause-on-invariance-fail",
        default=False,
        action="store_true",
        help="Pause execution on invariance failure.",
    )
    parser.add_argument(
        "--rpc-uri",
        type=str,
        default="",
        help="The RPC URI of the chain.",
    )
    parser.add_argument(
        "--fork-block",
        type=int,
        default=-1,
        help="The block to fork on",
    )
    parser.add_argument(
        "--chain-host",
        type=str,
        default="",
        help="The host to bind for the anvil chain. Defaults to 127.0.0.1.",
    )
    parser.add_argument(
        "--chain-port",
        type=int,
        default=-1,
        help="The port to run anvil on.",
    )
    parser.add_argument(
        "--rng-seed",
        type=int,
        default=-1,
        help="The random seed to use for the fuzz run.",
    )

    # Use system arguments if none were passed
    if argv is None:
        argv = sys.argv

    return namespace_to_args(parser.parse_args())


if __name__ == "__main__":
    main()
