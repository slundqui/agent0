"""Helper function for running random fuzz bots."""

from __future__ import annotations

import logging
from typing import Callable, Sequence

from eth_typing import ChecksumAddress
from fixedpointmath import FixedPoint
from numpy.random import Generator
from pypechain.core import PypechainCallException

from agent0 import Chain, Hyperdrive, LocalChain, LocalHyperdrive, PolicyZoo
from agent0.core.base.make_key import make_private_key
from agent0.core.hyperdrive.interactive.hyperdrive_agent import HyperdriveAgent
from agent0.ethpy.base import set_anvil_account_balance
from agent0.hyperfuzz import FuzzAssertionException
from agent0.hyperfuzz.system_fuzz.invariant_checks import run_invariant_checks
from agent0.hyperlogs.rollbar_utilities import log_rollbar_exception

ONE_HOUR_IN_SECONDS = 60 * 60
ONE_DAY_IN_SECONDS = ONE_HOUR_IN_SECONDS * 24
ONE_YEAR_IN_SECONDS = 52 * 7 * ONE_DAY_IN_SECONDS
ONE_YEAR_IN_HOURS = 52 * 7 * 24

# Fuzz ranges, defined as tuples of (min, max)

INITIAL_LIQUIDITY_RANGE: tuple[float, float] = (10, 100_000)
INITIAL_VAULT_SHARE_PRICE_RANGE: tuple[float, float] = (0.5, 2.5)
MINIMUM_SHARE_RESERVES_RANGE: tuple[float, float] = (0.1, 1)
MINIMUM_TRANSACTION_AMOUNT_RANGE: tuple[float, float] = (0.1, 10)
CIRCUIT_BREAKER_DELTA_RANGE: tuple[float, float] = (0.15, 2)

# Position and checkpoint duration are in units of hours, as
# the `factory_checkpoint_duration_resolution` is 1 hour
POSITION_DURATION_HOURS_RANGE: tuple[int, int] = (91, 2 * ONE_YEAR_IN_HOURS)
CHECKPOINT_DURATION_HOURS_RANGE: tuple[int, int] = (1, 24)

# The initial time stretch APR
INITIAL_TIME_STRETCH_APR_RANGE: tuple[float, float] = (0.005, 0.5)
# The variable rate to set after each episode
VARIABLE_RATE_RANGE: tuple[float, float] = (0, 1)
# How much to advance time between episodes
ADVANCE_TIME_SECONDS_RANGE: tuple[int, int] = (0, ONE_DAY_IN_SECONDS)
# The fee percentage. The range controls all 4 fees
FEE_RANGE: tuple[float, float] = (0.0001, 0.2)

# Special case for checking block to block lp share price
LP_SHARE_PRICE_VARIABLE_RATE_RANGE: tuple[float, float] = (0, 0.1)
LP_SHARE_PRICE_FLAT_FEE_RANGE: tuple[float, float] = (0, 0)
LP_SHARE_PRICE_CURVE_FEE_RANGE: tuple[float, float] = (0, 0)
LP_SHARE_PRICE_GOVERNANCE_LP_FEE_RANGE: tuple[float, float] = (0, 0)
LP_SHARE_PRICE_GOVERNANCE_ZOMBIE_FEE_RANGE: tuple[float, float] = (0, 0)


# pylint: disable=too-many-locals
def generate_fuzz_hyperdrive_config(rng: Generator, lp_share_price_test: bool, steth: bool) -> LocalHyperdrive.Config:
    """Fuzz over hyperdrive config.

    Arguments
    ---------
    rng: np.random.Generator
        Random number generator.
    lp_share_price_test: bool
        If True, uses lp share price test fuzz parameters.
    steth: bool
        If True, uses steth instead of erc4626

    Returns
    -------
    LocalHyperdrive.Config
        Fuzzed hyperdrive config.
    """
    # Position duration must be a multiple of checkpoint duration
    # To do this, we calculate the number of checkpoints per position
    # and adjust the position duration accordingly.
    position_duration_hours = int(rng.integers(*POSITION_DURATION_HOURS_RANGE))
    checkpoint_duration_hours = int(rng.integers(*CHECKPOINT_DURATION_HOURS_RANGE))

    # Checkpoint duration must be a multiple of `factory_checkpoint_duration_resolution`
    checkpoints_per_position_duration = position_duration_hours // checkpoint_duration_hours
    position_duration_hours = checkpoint_duration_hours * checkpoints_per_position_duration
    # There's a chance the new position duration was truncated to be less than the minimum
    # If that's the case, we use the ceil instead.
    if position_duration_hours < POSITION_DURATION_HOURS_RANGE[0]:
        position_duration_hours = checkpoint_duration_hours * (checkpoints_per_position_duration + 1)

    # Sanity check
    assert POSITION_DURATION_HOURS_RANGE[0] <= position_duration_hours <= POSITION_DURATION_HOURS_RANGE[1]

    # Convert checkpoint duration and position duration to seconds
    position_duration = position_duration_hours * ONE_HOUR_IN_SECONDS
    checkpoint_duration = checkpoint_duration_hours * ONE_HOUR_IN_SECONDS

    initial_time_stretch_apr = FixedPoint(rng.uniform(*INITIAL_TIME_STRETCH_APR_RANGE))

    if lp_share_price_test:
        variable_rate_range = LP_SHARE_PRICE_VARIABLE_RATE_RANGE
        flat_fee_range = LP_SHARE_PRICE_FLAT_FEE_RANGE
        curve_fee_range = LP_SHARE_PRICE_CURVE_FEE_RANGE
        governance_lp_fee_range = LP_SHARE_PRICE_GOVERNANCE_LP_FEE_RANGE
        governance_zombie_fee_range = LP_SHARE_PRICE_GOVERNANCE_ZOMBIE_FEE_RANGE
    else:
        variable_rate_range = VARIABLE_RATE_RANGE
        flat_fee_range = FEE_RANGE
        curve_fee_range = FEE_RANGE
        governance_lp_fee_range = FEE_RANGE
        governance_zombie_fee_range = FEE_RANGE

    # Generate flat fee in terms of APR
    flat_fee = FixedPoint(rng.uniform(*flat_fee_range) * (position_duration / ONE_YEAR_IN_SECONDS))

    # Steth expects an exact minimum share reserves and minimum transaction amount.
    if steth:
        minimum_share_reserves = FixedPoint("0.001")
        minimum_transaction_amount = FixedPoint("0.001")
    else:
        minimum_share_reserves = FixedPoint(rng.uniform(*MINIMUM_SHARE_RESERVES_RANGE))
        minimum_transaction_amount = FixedPoint(rng.uniform(*MINIMUM_TRANSACTION_AMOUNT_RANGE))

    return LocalHyperdrive.Config(
        # Initial hyperdrive config
        initial_liquidity=FixedPoint(rng.uniform(*INITIAL_LIQUIDITY_RANGE)),
        initial_fixed_apr=initial_time_stretch_apr,
        initial_time_stretch_apr=initial_time_stretch_apr,
        initial_variable_rate=FixedPoint(rng.uniform(*variable_rate_range)),
        minimum_share_reserves=minimum_share_reserves,
        minimum_transaction_amount=minimum_transaction_amount,
        circuit_breaker_delta=FixedPoint(rng.uniform(*CIRCUIT_BREAKER_DELTA_RANGE)),
        position_duration=position_duration,
        checkpoint_duration=checkpoint_duration,
        curve_fee=FixedPoint(rng.uniform(*curve_fee_range)),
        flat_fee=flat_fee,
        governance_lp_fee=FixedPoint(rng.uniform(*governance_lp_fee_range)),
        governance_zombie_fee=FixedPoint(rng.uniform(*governance_zombie_fee_range)),
        deploy_type=LocalHyperdrive.DeployType.ERC4626 if not steth else LocalHyperdrive.DeployType.STETH,
    )


def run_fuzz_bots(
    chain: Chain,
    hyperdrive_pools: Hyperdrive | Sequence[Hyperdrive],
    check_invariance: bool,
    num_random_agents: int | None = None,
    num_random_hold_agents: int | None = None,
    base_budget_per_bot: FixedPoint | None = None,
    eth_budget_per_bot: FixedPoint | None = None,
    slippage_tolerance: FixedPoint | None = None,
    raise_error_on_crash: bool = False,
    raise_error_on_failed_invariance_checks: bool = False,
    ignore_raise_error_func: Callable[[Exception], bool] | None = None,
    minimum_avg_agent_base: FixedPoint | None = None,
    minimum_avg_agent_eth: FixedPoint | None = None,
    log_to_rollbar: bool = True,
    run_async: bool = False,
    random_advance_time: bool = False,
    random_variable_rate: bool = False,
    num_iterations: int | None = None,
    lp_share_price_test: bool = False,
    whale_accounts: dict[ChecksumAddress, ChecksumAddress] | None = None,
) -> None:
    """Runs fuzz bots on a hyperdrive pool.

    Arguments
    ---------
    chain: Chain
        The chain to run the bots on.
    hyperdrive_pools: Hyperdrive | Sequence[Hyperdrive]
        The hyperdrive pool(s) to run the bots on.
    check_invariance: bool
        If True, will run invariance checks after each set of trades.
    num_random_agents: int | None, optional
        The number of random agents to create. Defaults to 2.
    num_random_hold_agents: int | None, optional
        The number of random agents to create. Defaults to 2.
    base_budget_per_bot: FixedPoint | None, optional
        The base budget per bot. Defaults to 10_000_000
    eth_budget_per_bot: FixedPoint | None, optional
        The ETH budget per bot. Defaults to 1_000
    slippage_tolerance: FixedPoint | None, optional
        The slippage tolerance. Defaults to 1% slippage
    raise_error_on_crash: bool, optional
        If True, will exit the process if a bot crashes. Defaults to False.
    raise_error_on_failed_invariance_checks: bool, optional
        If True, will exit the process if the pool fails an invariance check. Defaults to False.
    ignore_raise_error_func: Callable[[Exception], bool] | None, optional
        A function that determines if an exception should be ignored when raising error on crash.
        The function takes an exception as an an argument and returns True if the exception
        should be ignored. Defaults to raising all errors.
    minimum_avg_agent_base: FixedPoint | None, optional
        The minimum average agent base. Will refund bots if average agent base drops below this.
        Defaults to 1/10 of base_budget_per_bot
    minimum_avg_agent_eth: FixedPoint | None, optional
        The minimum average agent eth. Will refund bots if average agent base drops below this.
        Defaults to 1/10 of eth_budget_per_bot
    log_to_rollbar: bool, optional
        If True, log errors rollbar. Defaults to True.
    run_async: bool, optional
        If True, will run the bots asynchronously. Defaults to False.
    random_advance_time: bool, optional
        If True, will advance the time randomly between sets of trades. Defaults to False.
    random_variable_rate: bool, optional
        If True, will randomly change the rate between sets of trades. Defaults to False.
    num_iterations: int | None, optional
        The number of iterations to run. Defaults to None (infinite)
    lp_share_price_test: bool, optional
        If True, will test the LP share price. Defaults to False.
    whale_accounts: dict[ChecksumAddress, ChecksumAddress] | None, optional
        A mapping between token -> whale addresses to use to fund the fuzz agent.
        If the token is not in the mapping, fuzzing will attempt to call `mint` on
        the token contract. Defaults to an empty mapping.
    """
    # TODO cleanup
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    # Set defaults
    if num_random_agents is None:
        num_random_agents = 2
    if num_random_hold_agents is None:
        num_random_hold_agents = 2
    if base_budget_per_bot is None:
        base_budget_per_bot = FixedPoint("10_000_000")
    if eth_budget_per_bot is None:
        eth_budget_per_bot = FixedPoint("1_000")
    if slippage_tolerance is None:
        slippage_tolerance = FixedPoint("0.01")  # 1% slippage
    if minimum_avg_agent_base is None:
        minimum_avg_agent_base = base_budget_per_bot / FixedPoint(10)
    if minimum_avg_agent_eth is None:
        minimum_avg_agent_eth = eth_budget_per_bot / FixedPoint(10)

    if not isinstance(hyperdrive_pools, Sequence):
        hyperdrive_pools = [hyperdrive_pools]

    # Initialize agents
    agents: list[HyperdriveAgent] = []
    for _ in range(num_random_agents):
        # Initialize & fund agent using a random private key
        agent: HyperdriveAgent = chain.init_agent(
            private_key=make_private_key(),
            policy=PolicyZoo.random,
            policy_config=PolicyZoo.random.Config(
                slippage_tolerance=slippage_tolerance,
                trade_chance=FixedPoint("0.8"),
                randomly_ignore_slippage_tolerance=True,
            ),
        )
        # We're assuming we can fund the agent here
        for pool in hyperdrive_pools:
            agent.add_funds(
                base=base_budget_per_bot,
                eth=eth_budget_per_bot,
                pool=pool,
                whale_accounts=whale_accounts,
            )
            agent.set_max_approval(pool=pool)
        agents.append(agent)

    for _ in range(num_random_hold_agents):
        agent: HyperdriveAgent = chain.init_agent(
            private_key=make_private_key(),
            policy=PolicyZoo.random_hold,
            policy_config=PolicyZoo.random_hold.Config(
                slippage_tolerance=slippage_tolerance,
                trade_chance=FixedPoint("0.8"),
                randomly_ignore_slippage_tolerance=True,
                max_open_positions_per_pool=1_000,
            ),
        )
        # We're assuming we can fund the agent here
        for pool in hyperdrive_pools:
            agent.add_funds(
                base=base_budget_per_bot,
                eth=eth_budget_per_bot,
                pool=pool,
                whale_accounts=whale_accounts,
            )
            agent.set_max_approval(pool=pool)
        agents.append(agent)

    # Make trades until the user or agents stop us
    logging.info("Trading...")
    iteration = 0
    while True:
        if num_iterations is not None and iteration >= num_iterations:
            break
        iteration += 1
        # Execute the agent policies
        trades = []
        if run_async:
            # There are race conditions throughout that need to be fixed here
            raise NotImplementedError("Running async not implemented")
        for pool in hyperdrive_pools:
            logging.info("Trading on %s", pool.name)
            for agent in agents:
                # If we're checking invariance, and we're doing the lp share test,
                # we need to get the pending pool state here before the trades.
                pending_pool_state = None
                if check_invariance and lp_share_price_test:
                    pending_pool_state = pool.interface.get_hyperdrive_state("pending")

                # Execute trades
                agent_trade = []
                try:
                    agent_trade = agent.execute_policy_action(pool=pool)
                except PypechainCallException as exc:
                    if ignore_raise_error_func is None or not ignore_raise_error_func(exc):
                        # To ensure we log all errors, even when not from a trade contract call,
                        # we log the exception here.
                        # E.g., there's a crash when calling `interface.get_hyperdrive_state` from
                        # a contract call.
                        # TODO this can result in duplicate entries of the same error
                        log_rollbar_exception(
                            rollbar_log_prefix=f"Unexpected contract call error on pool {pool.name}",
                            exception=exc,
                            log_level=logging.ERROR,
                        )

                        if raise_error_on_crash:
                            raise exc
                    # Otherwise, we ignore crashes, we want the bot to keep trading
                    # These errors will get logged regardless

                trades.append(agent_trade)

                # Check invariance on every iteration
                if check_invariance:
                    latest_block = pool.interface.get_block("latest")
                    latest_block_number = latest_block.get("number", None)
                    if latest_block_number is None:
                        raise AssertionError("Block has no number.")
                    # pylint: disable=protected-access
                    fuzz_exceptions = run_invariant_checks(
                        check_block_data=latest_block,
                        interface=pool.interface,
                        log_to_rollbar=log_to_rollbar,
                        rollbar_log_level_threshold=chain.config.rollbar_log_level_threshold,
                        rollbar_log_filter_func=chain.config.rollbar_log_filter_func,
                        lp_share_price_test=lp_share_price_test,
                        crash_report_additional_info=pool._crash_report_additional_info,
                        log_anvil_state_dump=chain.config.log_anvil_state_dump,
                        pool_name=pool.name,
                        pending_pool_state=pending_pool_state,
                        check_price_spike=False,
                    )
                    if len(fuzz_exceptions) > 0 and raise_error_on_failed_invariance_checks:
                        # If we have an ignore function, we filter exceptions
                        if ignore_raise_error_func is not None:
                            fuzz_exceptions = [e for e in fuzz_exceptions if not ignore_raise_error_func(e)]
                        # Do nothing if no exceptions
                        # If single failure, we raise it by itself
                        if len(fuzz_exceptions) == 1:
                            raise fuzz_exceptions[0]
                        if len(fuzz_exceptions) > 1:
                            # Otherwise, we raise a new fuzz assertion exception wht the list of exceptions
                            raise FuzzAssertionException(*fuzz_exceptions)

        # Logs trades
        logging.debug([[trade.__name__ for trade in agent_trade] for agent_trade in trades])

        # Check agent funds and refund if necessary
        assert len(agents) > 0
        for hyperdrive_pool in hyperdrive_pools:
            average_agent_base = sum(
                agent.get_wallet(pool=hyperdrive_pool).balance.amount for agent in agents
            ) / FixedPoint(len(agents))
            # TODO add eth balance to wallet output
            average_agent_eth = sum(
                hyperdrive_pool.interface.get_eth_base_balances(agent.account)[0] for agent in agents
            ) / FixedPoint(len(agents))

            # Update agent funds
            if (average_agent_base < minimum_avg_agent_base) or (average_agent_eth < minimum_avg_agent_eth):
                logging.info("Refunding agents...")
                if run_async:
                    raise NotImplementedError("Running async not implemented")
                try:
                    _ = [
                        agent.add_funds(
                            base=base_budget_per_bot,
                            eth=eth_budget_per_bot,
                            pool=hyperdrive_pool,
                            whale_accounts=whale_accounts,
                        )
                        for agent in agents
                    ]
                except ValueError as e:
                    # Look for the case when the whale doesn't have enough base to transfer, and
                    # ignore when refunding.
                    if "Whale does not have enough base to transfer." not in e.args[0]:
                        raise e

        if random_advance_time:
            # We only allow random advance time if the chain connected to the pool is a
            # LocalChain object
            if isinstance(chain, LocalChain):
                # The deployer pays gas for advancing time
                # We check the eth balance and refund if it runs low
                deployer_account = chain.get_deployer_account()
                deployer_agent_eth = hyperdrive_pools[0].interface.get_eth_base_balances(deployer_account)[0]
                if deployer_agent_eth < minimum_avg_agent_eth:
                    _ = set_anvil_account_balance(
                        hyperdrive_pools[0].interface.web3, deployer_account.address, eth_budget_per_bot.scaled_value
                    )
                # RNG should always exist, config's post_init should always
                # initialize an rng object
                assert chain.config.rng is not None
                # TODO should there be an upper bound for advancing time?
                random_time = int(chain.config.rng.integers(*ADVANCE_TIME_SECONDS_RANGE))
                chain.advance_time(random_time, create_checkpoints=True)
            else:
                raise ValueError("Random advance time only allowed for pools deployed on LocalChain")

        if random_variable_rate:
            # This will change an underlying yield source twice if pools share the same underlying
            # yield source
            if lp_share_price_test:
                variable_rate_range = LP_SHARE_PRICE_VARIABLE_RATE_RANGE
            else:
                variable_rate_range = VARIABLE_RATE_RANGE
            for hyperdrive_pool in hyperdrive_pools:
                if isinstance(hyperdrive_pool, LocalHyperdrive):
                    # RNG should always exist, config's post_init should always
                    # initialize an rng object
                    assert hyperdrive_pool.chain.config.rng is not None
                    random_rate = FixedPoint(hyperdrive_pool.chain.config.rng.uniform(*variable_rate_range))
                    hyperdrive_pool.set_variable_rate(random_rate)
                else:
                    raise ValueError("Random variable rate only allowed for LocalHyperdrive pools")
