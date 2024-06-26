"""Test utils specific for system tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from fixedpointmath import FixedPoint

if TYPE_CHECKING:
    from agent0.core.hyperdrive.interactive import LocalHyperdrive
    from agent0.core.hyperdrive.policies import HyperdriveBasePolicy


def expect_failure_with_funded_bot(in_hyperdrive: LocalHyperdrive, in_policy: Type[HyperdriveBasePolicy]):
    """Run a funded bot and throw an error if the bot was successful.

    Arguments
    ---------
    in_hyperdrive: LocalHyperdrive
        The local hyperdrive object to run.
    in_policy: HyperdriveBasePolicy
        The policy that we expect to fail.
    """
    run_with_funded_bot(in_hyperdrive, in_policy)

    # If this reaches this point, the agent was successful, which means this test should fail
    assert False, "Agent was successful with known invalid trade"


def expect_failure_with_non_funded_bot(in_hyperdrive: LocalHyperdrive, in_policy: Type[HyperdriveBasePolicy]):
    """Run a non-funded bot and expect it to fail with a known invalid trade.

    Arguments
    ---------
    in_hyperdrive: LocalHyperdrive
        The local hyperdrive object to run.
    in_policy: HyperdriveBasePolicy
        The policy that we expect to fail.
    """
    run_with_non_funded_bot(in_hyperdrive, in_policy)

    # If this reaches this point, the agent was successful, which means this test should fail
    assert False, "Agent was successful with known invalid trade"


def run_with_funded_bot(in_hyperdrive: LocalHyperdrive, in_policy: Type[HyperdriveBasePolicy]):
    """Run a funded bot and expect it to fail with a known invalid trade.

    Arguments
    ---------
    in_hyperdrive: LocalHyperdrive
        The local hyperdrive object to run.
    in_policy: HyperdriveBasePolicy
        The policy that we expect to fail.
    """
    agent = in_hyperdrive.chain.init_agent(
        base=FixedPoint(10_000_000),
        eth=FixedPoint(100),
        pool=in_hyperdrive,
        policy=in_policy,
        policy_config=in_policy.Config(),
    )

    while not agent.policy_done_trading:
        agent.execute_policy_action()


def run_with_non_funded_bot(in_hyperdrive: LocalHyperdrive, in_policy: Type[HyperdriveBasePolicy]):
    """Run a funded bot and expect it to fail with a known invalid trade.

    Arguments
    ---------
    in_hyperdrive: LocalHyperdrive
        The local hyperdrive object to run.
    in_policy: HyperdriveBasePolicy
        The policy that we expect to fail.
    """
    agent = in_hyperdrive.chain.init_agent(
        base=FixedPoint(0.001),
        eth=FixedPoint(100),
        pool=in_hyperdrive,
        policy=in_policy,
        policy_config=in_policy.Config(),
    )

    while not agent.policy_done_trading:
        agent.execute_policy_action()
