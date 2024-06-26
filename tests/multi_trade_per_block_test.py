"""System test for end to end usage of agent0 libraries."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
import pytest
from fixedpointmath import FixedPoint

from agent0.core.base import Trade
from agent0.core.hyperdrive import HyperdriveMarketAction, HyperdriveWallet
from agent0.core.hyperdrive.agent import add_liquidity_trade, open_long_trade, open_short_trade
from agent0.core.hyperdrive.interactive import LocalHyperdrive
from agent0.core.hyperdrive.policies import HyperdriveBasePolicy

if TYPE_CHECKING:
    from agent0.ethpy.hyperdrive import HyperdriveReadInterface


class MultiTradePolicy(HyperdriveBasePolicy):
    """An agent that submits multiple trades per block."""

    counter = 0

    def action(
        self, interface: HyperdriveReadInterface, wallet: HyperdriveWallet
    ) -> tuple[list[Trade[HyperdriveMarketAction]], bool]:
        """Open all trades for a fixed amount and closes them after, one at a time.

        Arguments
        ---------
        interface: HyperdriveReadInterface
            The trading market interface.
        wallet: HyperdriveWallet
            The agent's wallet.

        Returns
        -------
        tuple[list[HyperdriveMarketAction], bool]
            A tuple where the first element is a list of actions,
            and the second element defines if the agent is done trading
        """

        done_trading = False

        if self.counter == 0:
            # Adding liquidity to make other trades valid
            action_list: list[Trade[HyperdriveMarketAction]] = [
                add_liquidity_trade(FixedPoint(1_111_111)),
            ]
        elif self.counter == 1:
            # Adding in 3 trades at the same time:
            action_list: list[Trade[HyperdriveMarketAction]] = [
                add_liquidity_trade(FixedPoint(11_111)),
                open_long_trade(FixedPoint(22_222)),
                open_short_trade(FixedPoint(33_333)),
            ]
            done_trading = True
        else:
            # We want this bot to exit and crash after it's done the trades it needs to do
            # In this case, if this exception gets thrown, this means an invalid trade went through
            raise AssertionError("This policy's action shouldn't get called again after failure")

        self.counter += 1
        return action_list, done_trading


class TestMultiTradePerBlock:
    """Test pipeline from bots making trades to viewing the trades in the db."""

    # TODO split this up into different functions that work with tests
    # pylint: disable=too-many-locals, too-many-statements
    @pytest.mark.docker
    def test_multi_trade_per_block(
        self,
        fast_hyperdrive_fixture: LocalHyperdrive,
    ):
        """Runs the entire pipeline and checks the database at the end. All arguments are fixtures."""
        # TODO local_hyperdrive_pool is currently being run with automining. Hence, multiple trades
        # per block can't be tested until we can parameterize anvil running without automining.
        # For now, this is simply testing that the introduction of async trades doesn't break
        # when automining.

        agent = fast_hyperdrive_fixture.chain.init_agent(
            base=FixedPoint(10_000_000),
            eth=FixedPoint(100),
            pool=fast_hyperdrive_fixture,
            policy=MultiTradePolicy,
            policy_config=MultiTradePolicy.Config(),
        )

        while not agent.policy_done_trading:
            agent.execute_policy_action()

        # Ensure all 4 trades went through
        # 1. addLiquidity of 111_111 base
        # 2. addLiquidity of 11_111 base
        # 3. openLong of 22_222 base
        # 4. openShort of 33_333 bonds

        expected_number_of_transactions = 4

        trade_events: pd.DataFrame = agent.get_trade_events(coerce_float=False)
        assert len(trade_events == expected_number_of_transactions)
        assert "AddLiquidity" == trade_events["event_type"].iloc[0]
        ticker_ops = trade_events["event_type"].iloc[1:].to_list()
        assert "AddLiquidity" in ticker_ops
        assert "OpenLong" in ticker_ops
        assert "OpenShort" in ticker_ops
