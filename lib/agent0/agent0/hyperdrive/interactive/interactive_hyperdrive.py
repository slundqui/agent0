"""Defines the interactive hyperdrive class that encapsulates a hyperdrive pool."""
from __future__ import annotations

import asyncio
import os
from dataclasses import asdict, dataclass
from decimal import Decimal

import nest_asyncio
import pandas as pd
from chainsync import PostgresConfig
from chainsync.dashboard.usernames import build_user_mapping
from chainsync.db.base import add_addr_to_username, get_addr_to_username, get_username_to_user, initialize_session
from chainsync.db.hyperdrive import (
    get_checkpoint_info,
    get_pool_analysis,
    get_pool_config,
    get_pool_info,
    get_ticker,
    get_total_wallet_pnl_over_time,
    get_wallet_deltas,
    get_wallet_pnl,
)
from chainsync.exec import acquire_data, data_analysis
from eth_account.account import Account
from eth_typing import ChecksumAddress
from eth_utils.address import to_checksum_address
from ethpy import EthConfig
from ethpy.base import set_anvil_account_balance, smart_contract_transact
from ethpy.hyperdrive import BASE_TOKEN_SYMBOL, DeployedHyperdrivePool, ReceiptBreakdown, deploy_hyperdrive_from_factory
from ethpy.hyperdrive.api import HyperdriveInterface
from fixedpointmath import FixedPoint
from hypertypes import Fees, PoolConfig
from web3.constants import ADDRESS_ZERO

from agent0.base.make_key import make_private_key
from agent0.hyperdrive.agents import HyperdriveAgent
from agent0.hyperdrive.crash_report import get_anvil_state_dump, log_hyperdrive_crash_report
from agent0.hyperdrive.exec import async_execute_agent_trades, set_max_approval
from agent0.hyperdrive.state import HyperdriveActionType, TradeResult, TradeStatus

from .chain import Chain
from .event_types import (
    AddLiquidity,
    CloseLong,
    CloseShort,
    CreateCheckpoint,
    OpenLong,
    OpenShort,
    RedeemWithdrawalShares,
    RemoveLiquidity,
)
from .interactive_hyperdrive_agent import InteractiveHyperdriveAgent
from .interactive_hyperdrive_policy import InteractiveHyperdrivePolicy

# In order to support both scripts and jupyter notebooks with underlying async functions,
# we use the nest_asyncio package so that we can execute asyncio.run within a running event loop.
nest_asyncio.apply()


class InteractiveHyperdrive:
    """Hyperdrive class that supports an interactive interface for running tests and experiments."""

    # Lots of attributes in config
    # pylint: disable=too-many-instance-attributes
    @dataclass
    class Config:
        """
        The configuration for the initial pool configuration

        Attributes
        ----------
        initial_liquidity : FixedPoint
            The amount of money to be provided by the `deploy_account` for initial pool liquidity.
        initial_variable_rate: FixedPoint
            The starting variable rate for an underlying yield source.
        initial_fixed_rate : FixedPoint
            The fixed rate of the pool on initialization.
        initial_share_price : FixedPoint
            The initial share price
        minimum_share_reserves : FixedPoint
            The minimum share reserves
        minimum_transaction_amount : FixedPoint
            The minimum amount of tokens that a position can be opened or closed with.
        precision_threshold : int
            The amount of precision expected to lose due to exponentiation implementation.
        position_duration: int
            The duration of a position prior to maturity (in seconds)
        checkpoint_duration: int
            The duration of a checkpoint (in seconds)
        time_stretch: FixedPoint
            A parameter which decreases slippage around a target rate
        curve_fee: FixedPoint
            The LP fee applied to the curve portion of a trade.
        flat_fee: FixedPoint
            The LP fee applied to the flat portion of a trade.
        governance_fee: FixedPoint
            The portion of the LP fee that goes to governance.
        max_curve_fee: FixedPoint
            The upper bound on the curve fee that governance can set.
        max_flat_fee: FixedPoint
            The upper bound on the flat fee that governance can set.
        max_governance_fee: FixedPoint
            The upper bound on the governance fee that governance can set.
        """

        initial_liquidity: FixedPoint = FixedPoint(100_000_000)
        initial_variable_rate: FixedPoint = FixedPoint("0.05")
        initial_fixed_rate: FixedPoint = FixedPoint("0.05")
        # Initial Pool Config variables
        initial_share_price: FixedPoint = FixedPoint(1)
        minimum_share_reserves: FixedPoint = FixedPoint(10)
        minimum_transaction_amount: FixedPoint = FixedPoint("0.001")
        # TODO this likely should be FixedPoint
        precision_threshold: int = int(1e14)
        position_duration: int = 604800  # 1 week
        checkpoint_duration: int = 3600  # 1 hour
        time_stretch: FixedPoint | None = None
        curve_fee = FixedPoint("0.1")  # 10%
        flat_fee = FixedPoint("0.0005")  # 0.05%
        governance_fee = FixedPoint("0.15")  # 15%
        max_curve_fee = FixedPoint("0.3")  # 30%
        max_flat_fee = FixedPoint("0.0015")  # 0.15%
        max_governance_fee = FixedPoint("0.30")  # 30%

        def __post_init__(self):
            if self.time_stretch is None:
                self.time_stretch = FixedPoint(1) / (
                    FixedPoint("5.24592") / (FixedPoint("0.04665") * (self.initial_fixed_rate * FixedPoint(100)))
                )

    def __init__(self, chain: Chain, config: Config | None = None):
        """Constructor for the interactive hyperdrive agent.

        Arguments
        ---------
        chain: Chain
            The chain object to launch hyperdrive on
        config: Config | None
            The configuration for the initial pool configuration
        """
        if config is None:
            config = self.Config()

        # Define agent0 configs with this setup
        # TODO currently getting the path based on this file's path
        # This requires the entire monorepo to be check out, and will likely not work when
        # installing agent0 by itself.
        # This should get fixed when abis are exported in hypertypes.
        full_path = os.path.realpath(__file__)
        current_file_dir, _ = os.path.split(full_path)
        abi_dir = os.path.join(current_file_dir, "..", "..", "..", "..", "..", "packages", "hyperdrive", "src", "abis")

        self.eth_config = EthConfig(artifacts_uri="not_used", rpc_uri=chain.rpc_uri, abi_dir=abi_dir)
        # Deploys a hyperdrive factory + pool on the chain
        self._deployed_hyperdrive = self._deploy_hyperdrive(config, chain, self.eth_config.abi_dir)
        self.hyperdrive_interface = HyperdriveInterface(
            self.eth_config,
            self._deployed_hyperdrive.hyperdrive_contract_addresses,
        )
        # At this point, we've deployed hyperdrive, so we want to save the block where it was deployed
        # for the data pipeline
        self._deploy_block_number = self.hyperdrive_interface.get_block_number(
            self.hyperdrive_interface.get_current_block()
        )

        # Make a copy of the dataclass to avoid changing the base class
        postgres_config = PostgresConfig(**asdict(chain.postgres_config))
        # Update the database field to use a unique name for this pool using the hyperdrive contract address
        postgres_config.POSTGRES_DB = "interactive-hyperdrive-" + str(
            self.hyperdrive_interface.hyperdrive_contract.address
        )

        self.db_session = initialize_session(postgres_config, ensure_database_created=True)

        # Keep track of how much base have been minted per agent
        self._initial_funds: dict[ChecksumAddress, FixedPoint] = {}

    def __del__(self):
        # Attempt to close the session
        # These functions will raise errors if the session is already closed
        try:
            self.db_session.close()
        # Never throw exception in destructor
        except Exception:  # pylint: disable=broad-except
            pass

    def _deploy_hyperdrive(self, config: Config, chain: Chain, abi_dir) -> DeployedHyperdrivePool:
        # sanity check (also for type checking), should get set in __post_init__
        assert config.time_stretch is not None

        initial_pool_config = PoolConfig(
            "",  # will be determined in the deploy function
            ADDRESS_ZERO,  # address(0), this address needs to be in a valid address format
            bytes(32),  # bytes32(0)
            config.initial_share_price.scaled_value,
            config.minimum_share_reserves.scaled_value,
            config.minimum_transaction_amount.scaled_value,
            config.precision_threshold,
            config.position_duration,
            config.checkpoint_duration,
            config.time_stretch.scaled_value,
            "",  # will be determined in the deploy function
            "",  # will be determined in the deploy function
            Fees(config.curve_fee.scaled_value, config.flat_fee.scaled_value, config.governance_fee.scaled_value),
        )

        max_fees = Fees(
            config.max_curve_fee.scaled_value, config.max_flat_fee.scaled_value, config.max_governance_fee.scaled_value
        )

        return deploy_hyperdrive_from_factory(
            chain.rpc_uri,
            abi_dir,
            chain.get_deployer_account_private_key(),
            config.initial_liquidity,
            config.initial_variable_rate,
            config.initial_fixed_rate,
            initial_pool_config,
            max_fees,
        )

    def init_agent(
        self,
        base: FixedPoint | None = None,
        eth: FixedPoint | None = None,
        name: str | None = None,
    ) -> InteractiveHyperdriveAgent:
        """Initializes an agent with initial funding and a logical name.

        Arguments
        ---------
        base: FixedPoint
            The amount of base to fund the agent with. Defaults to 0.
        eth: FixedPoint
            The amount of ETH to fund the agent with. Defaults to 10.
        name: str
            The name of the agent. Defaults to the wallet address.
        """
        if base is None:
            base = FixedPoint(0)
        if eth is None:
            eth = FixedPoint(10)
        out_agent = InteractiveHyperdriveAgent(base=base, eth=eth, name=name, pool=self)
        return out_agent

    ### Database methods
    # These methods expose the underlying chainsync getter methods with minimal processing
    # TODO expand in docstrings the columns of the output dataframe

    def get_pool_config(self, coerce_float: bool = True) -> pd.Series:
        """Get the pool config and returns as a pandas series.

        Arguments
        ---------
        coerce_float : bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Series
            A pandas series that consists of the deployed pool config.
        """
        # Underlying function returns a dataframe, but this is assuming there's a single
        # pool config for this object.
        return get_pool_config(self.db_session, coerce_float=coerce_float).iloc[0]

    def get_pool_info(self, coerce_float: bool = True) -> pd.DataFrame:
        """Get the pool info (and additional info) per block and returns as a pandas dataframe.

        Arguments
        ---------
        coerce_float : bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Dataframe
            A pandas dataframe that consists of the pool info per block.
        """
        pool_info = get_pool_info(self.db_session, coerce_float=coerce_float)
        pool_analysis = get_pool_analysis(self.db_session, coerce_float=coerce_float, return_timestamp=False)
        pool_info = pool_info.merge(pool_analysis, how="left", on="block_number")
        return pool_info

    def get_checkpoint_info(self, coerce_float: bool = True) -> pd.DataFrame:
        """Get the previous checkpoint infos per block and returns as a pandas dataframe.

        Arguments
        ---------
        coerce_float : bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Dataframe
            A pandas dataframe that consists of the checkpoint info per block.
        """
        # TODO checkpoint info doesn't play nice with advancing time.
        # This is because we don't create checkpoints when we advance time.
        # https://github.com/delvtech/agent0/issues/1106
        out = get_checkpoint_info(self.db_session, coerce_float=coerce_float)
        return out

    def _add_username_to_dataframe(self, df: pd.DataFrame, addr_column: str):
        addr_to_username = get_addr_to_username(self.db_session)
        username_to_user = get_username_to_user(self.db_session)

        # Get corresponding usernames
        usernames = build_user_mapping(df[addr_column], addr_to_username, username_to_user)["username"]
        df.insert(df.columns.get_loc(addr_column), "username", usernames)
        return df

    def _adjust_base_positions(self, in_df: pd.DataFrame, value_column: str, coerce_float: bool):
        out_df = in_df.copy()
        for address, initial_balance in self._initial_funds.items():
            row_idxs = (out_df["wallet_address"] == address) & (out_df["base_token_type"] == BASE_TOKEN_SYMBOL)
            if coerce_float:
                out_df.loc[row_idxs, value_column] += float(initial_balance)
            else:
                out_df.loc[row_idxs, value_column] += Decimal(str(initial_balance))
        return out_df

    def get_current_wallet(self, coerce_float: bool = True) -> pd.DataFrame:
        """Gets the current wallet positions of all agents and their corresponding pnl
        and returns as a pandas dataframe.

        Arguments
        ---------
        coerce_float : bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Dataframe
            timestamp : pd.Timestamp
                The block timestamp of the entry.
            block_number : int
                The block number of the entry.
            username : str
                The username of the entry.
            wallet_address : str
                The wallet address of the entry.
            token_type : str
                A string specifying the token type. Longs and shorts are encoded as `LONG-{maturity_time}`.
            position : Decimal | float
                The current value of the token of the agent at the specified block number.
            pnl: Decimal | float
                The current pnl of the token of the agent at the specified block number.
            base_token_type : str
                A string specifying the type of the token.
            maturity_time : Decimal | float
                The maturity time of the token in epoch seconds. Can be NaN to denote not applicable.
            latest_block_update: int
                The last block number that the position was updated.
        """
        # TODO potential improvement is to pivot the table so that columns are the token type
        # Makes this data easier to work with
        # https://github.com/delvtech/agent0/issues/1106
        out = get_wallet_pnl(self.db_session, start_block=-1, coerce_float=coerce_float)
        # DB only stores final delta for base, we calculate actual base based on how much funds
        # were added in all
        out = self._adjust_base_positions(out, "value", coerce_float)
        # Rename column to match get_wallet_positions
        out = out.rename(columns={"value": "position"})
        # Add usernames
        out = self._add_username_to_dataframe(out, "wallet_address")
        # Filter and order columns
        out = out[
            [
                "timestamp",
                "block_number",
                "username",
                "wallet_address",
                "token_type",
                "position",
                "pnl",
                "base_token_type",
                "maturity_time",
                "latest_block_update",
            ]
        ]
        return out

    def get_ticker(self, coerce_float: bool = True) -> pd.DataFrame:
        """Gets the ticker history of all trades and the corresponding token deltas for each trade.

        Arguments
        ---------
        coerce_float : bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Dataframe
            timestamp : pd.Timestamp
                The block timestamp of the entry.
            block_number : int
                The block number of the entry.
            username : str
                The username of the entry.
            wallet_address : str
                The wallet address of the entry.
            trade_type : str
                The trade that the agent made.
            token_diffs : list[str]
                A list of token diffs for each trade. Each token diff is encoded as "<base_token_type>: <amount>"
        """
        out = get_ticker(self.db_session, coerce_float=coerce_float).drop("id", axis=1)
        out = self._add_username_to_dataframe(out, "wallet_address")
        out = out[
            [
                "timestamp",
                "block_number",
                "username",
                "wallet_address",
                "trade_type",
                "token_diffs",
            ]
        ]
        return out

    def get_wallet_positions(self, coerce_float: bool = True) -> pd.DataFrame:
        """Get a dataframe summarizing all wallet deltas and positions
        and returns as a pandas dataframe.

        Arguments
        ---------
        coerce_float : bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Dataframe
            timestamp : pd.Timestamp
                The block timestamp of the entry.
            block_number : int
                The block number of the entry.
            username : str
                The username of the entry.
            wallet_address : str
                The wallet address of the entry.
            token_type : str
                A string specifying the token type. Longs and shorts are encoded as `LONG-{maturity_time}`.
            position : Decimal | float
                The current value of the token of the agent at the specified block number.
            delta: Decimal | float
                The change in value of the token of the agent at the specified block number.
            base_token_type : str
                A string specifying the type of the token.
            maturity_time : Decimal | float
                The maturity time of the token in epoch seconds. Can be NaN to denote not applicable.
            transaction_hash: str
                The transaction hash that resulted in the deltas.
        """
        # We gather all deltas and calculate the current positions here
        # If computing this is too slow, we can get current positions from
        # the wallet_pnl table and left merge with the deltas
        out = get_wallet_deltas(self.db_session, coerce_float=coerce_float)
        out["position"] = out.groupby(["wallet_address", "token_type"])["delta"].transform(pd.Series.cumsum)

        # DB only stores final delta for base, we calculate actual base based on how much funds
        # were added in all
        out = self._adjust_base_positions(out, "position", coerce_float)
        # Add usernames
        out = self._add_username_to_dataframe(out, "wallet_address")
        # Filter and order columns
        out = out[
            [
                "timestamp",
                "block_number",
                "username",
                "wallet_address",
                "token_type",
                "position",
                "delta",
                "base_token_type",
                "maturity_time",
                "transaction_hash",
            ]
        ]
        return out

    def get_total_wallet_pnl_over_time(self, coerce_float: bool = True) -> pd.DataFrame:
        """Gets total pnl for each wallet for each block, aggregated across all open positions.

        Arguments
        ---------
        coerce_float : bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Dataframe
            timestamp : pd.Timestamp
                The block timestamp of the entry.
            block_number : int
                The block number of the entry.
            username : str
                The username of the entry.
            wallet_address : str
                The wallet address of the entry.
            pnl : Decimal | float
                The total pnl of the agent at the specified block number.
        """
        out = get_total_wallet_pnl_over_time(self.db_session, coerce_float=coerce_float)
        out = self._add_username_to_dataframe(out, "wallet_address")
        out = out[
            [
                "timestamp",
                "block_number",
                "username",
                "wallet_address",
                "pnl",
            ]
        ]
        return out

    ### Private agent methods ###

    def _init_agent(self, base: FixedPoint, eth: FixedPoint, name: str | None) -> HyperdriveAgent:
        agent_private_key = make_private_key()
        # Setting the budget to 0 here, `_add_funds` will take care of updating the wallet
        agent = HyperdriveAgent(
            Account().from_key(agent_private_key), policy=InteractiveHyperdrivePolicy(budget=FixedPoint(0))
        )

        # Fund agent
        if eth > 0 or base > 0:
            self._add_funds(agent, base, eth)

        # establish max approval for the hyperdrive contract
        asyncio.gather(
            set_max_approval(
                [agent],
                self.hyperdrive_interface.web3,
                self.hyperdrive_interface.base_token_contract,
                str(self.hyperdrive_interface.hyperdrive_contract.address),
            )
        )

        # Register the username if it was provided
        if name is not None:
            add_addr_to_username(name, [agent.address], self.db_session)
        return agent

    def _add_funds(self, agent: HyperdriveAgent, base: FixedPoint, eth: FixedPoint) -> None:
        if eth > FixedPoint(0):
            # Eth is a set balance call
            eth_balance, _ = self.hyperdrive_interface.get_eth_base_balances(agent)
            new_eth_balance = eth_balance + eth
            _ = set_anvil_account_balance(self.hyperdrive_interface.web3, agent.address, new_eth_balance.scaled_value)

        if base > FixedPoint(0):
            # We mint base
            _ = smart_contract_transact(
                self.hyperdrive_interface.web3,
                self.hyperdrive_interface.base_token_contract,
                agent,
                "mint(address,uint256)",
                agent.checksum_address,
                base.scaled_value,
            )
            # Update the agent's wallet balance
            agent.wallet.balance.amount += base

            # Keep track of how much base has been minted for each agent
            if agent.address in self._initial_funds:
                self._initial_funds[agent.address] += base
            else:
                self._initial_funds[agent.address] = base

        # TODO do we want to report a status here?

    def _handle_trade_result(self, trade_results: list[TradeResult]) -> ReceiptBreakdown:
        # Sanity check, should only be one trade result
        assert len(trade_results) == 1
        trade_result = trade_results[0]
        if trade_result.status == TradeStatus.FAIL:
            assert trade_result.exception is not None
            # TODO when we allow for async, we likely would want to ignore slippage checks here
            # We only get anvil state dump here, since it's an on chain call
            # and we don't want to do it when e.g., slippage happens
            trade_result.anvil_state = get_anvil_state_dump(self.hyperdrive_interface.web3)
            # Defaults to CRITICAL
            log_hyperdrive_crash_report(trade_result, crash_report_to_file=True)
            raise trade_result.exception
        assert trade_result.status == TradeStatus.SUCCESS
        assert len(trade_results) == 1
        tx_receipt = trade_results[0].tx_receipt
        assert tx_receipt is not None
        return tx_receipt

    def _run_data_pipeline(self) -> None:
        # TODO these functions are not thread safe, need to fix if we expose async functions
        acquire_data(
            start_block=self._deploy_block_number,  # Start block is the block hyperdrive was deployed
            eth_config=self.eth_config,
            db_session=self.db_session,
            contract_addresses=self.hyperdrive_interface.addresses,
            exit_on_catch_up=True,
        )
        data_analysis(
            start_block=self._deploy_block_number,
            eth_config=self.eth_config,
            db_session=self.db_session,
            contract_addresses=self.hyperdrive_interface.addresses,
            exit_on_catch_up=True,
        )

    def _open_long(self, agent: HyperdriveAgent, base: FixedPoint) -> OpenLong:
        # Set the next action to open a long
        assert isinstance(agent.policy, InteractiveHyperdrivePolicy)
        agent.policy.set_next_action(HyperdriveActionType.OPEN_LONG, base)
        # TODO expose async here to the caller eventually
        trade_results: list[TradeResult] = asyncio.run(
            async_execute_agent_trades(self.hyperdrive_interface, [agent], False)
        )
        tx_receipt = self._handle_trade_result(trade_results)
        # TODO running the data pipeline here may be slow, perhaps we should
        # do it in the background or have an explicit call to load the db
        self._run_data_pipeline()
        # Build open long event from trade_result
        return OpenLong(
            trader=to_checksum_address(tx_receipt.trader),
            asset_id=tx_receipt.asset_id,
            maturity_time=tx_receipt.maturity_time_seconds,
            base_amount=tx_receipt.base_amount,
            share_price=tx_receipt.share_price,
            bond_amount=tx_receipt.bond_amount,
        )

    def _close_long(self, agent: HyperdriveAgent, maturity_time: int, bonds: FixedPoint) -> CloseLong:
        # Set the next action to open a long
        assert isinstance(agent.policy, InteractiveHyperdrivePolicy)
        agent.policy.set_next_action(HyperdriveActionType.CLOSE_LONG, bonds, maturity_time)
        # TODO expose async here to the caller eventually
        trade_results: list[TradeResult] = asyncio.run(
            async_execute_agent_trades(self.hyperdrive_interface, [agent], False)
        )
        tx_receipt = self._handle_trade_result(trade_results)
        # TODO running the data pipeline here may be slow, perhaps we should
        # do it in the background or have an explicit call to load the db
        self._run_data_pipeline()
        # Build open long event from trade_result
        return CloseLong(
            trader=to_checksum_address(tx_receipt.trader),
            asset_id=tx_receipt.asset_id,
            maturity_time=tx_receipt.maturity_time_seconds,
            base_amount=tx_receipt.base_amount,
            share_price=tx_receipt.share_price,
            bond_amount=tx_receipt.bond_amount,
        )

    def _open_short(self, agent: HyperdriveAgent, bonds: FixedPoint) -> OpenShort:
        # Set the next action to open a long
        assert isinstance(agent.policy, InteractiveHyperdrivePolicy)
        agent.policy.set_next_action(HyperdriveActionType.OPEN_SHORT, bonds)
        # TODO expose async here to the caller eventually
        trade_results: list[TradeResult] = asyncio.run(
            async_execute_agent_trades(self.hyperdrive_interface, [agent], False)
        )
        tx_receipt = self._handle_trade_result(trade_results)
        # TODO running the data pipeline here may be slow, perhaps we should
        # do it in the background or have an explicit call to load the db
        self._run_data_pipeline()
        # Build open long event from trade_result
        return OpenShort(
            trader=to_checksum_address(tx_receipt.trader),
            asset_id=tx_receipt.asset_id,
            maturity_time=tx_receipt.maturity_time_seconds,
            base_amount=tx_receipt.base_amount,
            share_price=tx_receipt.share_price,
            bond_amount=tx_receipt.bond_amount,
        )

    def _close_short(self, agent: HyperdriveAgent, maturity_time: int, bonds: FixedPoint) -> CloseShort:
        # Set the next action to open a long
        assert isinstance(agent.policy, InteractiveHyperdrivePolicy)
        agent.policy.set_next_action(HyperdriveActionType.CLOSE_SHORT, bonds, maturity_time=maturity_time)
        # TODO expose async here to the caller eventually
        trade_results: list[TradeResult] = asyncio.run(
            async_execute_agent_trades(self.hyperdrive_interface, [agent], False)
        )
        tx_receipt = self._handle_trade_result(trade_results)
        # TODO running the data pipeline here may be slow, perhaps we should
        # do it in the background or have an explicit call to load the db
        self._run_data_pipeline()
        # Build open long event from trade_result
        return CloseShort(
            trader=to_checksum_address(tx_receipt.trader),
            asset_id=tx_receipt.asset_id,
            maturity_time=tx_receipt.maturity_time_seconds,
            base_amount=tx_receipt.base_amount,
            share_price=tx_receipt.share_price,
            bond_amount=tx_receipt.bond_amount,
        )

    def _add_liquidity(self, agent: HyperdriveAgent, base: FixedPoint) -> AddLiquidity:
        # Set the next action to open a long
        assert isinstance(agent.policy, InteractiveHyperdrivePolicy)
        agent.policy.set_next_action(HyperdriveActionType.ADD_LIQUIDITY, base)
        # TODO expose async here to the caller eventually
        trade_results: list[TradeResult] = asyncio.run(
            async_execute_agent_trades(self.hyperdrive_interface, [agent], False)
        )
        tx_receipt = self._handle_trade_result(trade_results)
        # TODO running the data pipeline here may be slow, perhaps we should
        # do it in the background or have an explicit call to load the db
        self._run_data_pipeline()
        # Build open long event from trade_result
        return AddLiquidity(
            provider=to_checksum_address(tx_receipt.provider),
            lp_amount=tx_receipt.lp_amount,
            base_amount=tx_receipt.base_amount,
            share_price=tx_receipt.share_price,
            lp_share_price=tx_receipt.lp_share_price,
        )

    def _remove_liquidity(self, agent: HyperdriveAgent, shares: FixedPoint) -> RemoveLiquidity:
        # Set the next action to open a long
        assert isinstance(agent.policy, InteractiveHyperdrivePolicy)
        agent.policy.set_next_action(HyperdriveActionType.REMOVE_LIQUIDITY, shares)
        # TODO expose async here to the caller eventually
        trade_results: list[TradeResult] = asyncio.run(
            async_execute_agent_trades(self.hyperdrive_interface, [agent], False)
        )
        tx_receipt = self._handle_trade_result(trade_results)
        # TODO running the data pipeline here may be slow, perhaps we should
        # do it in the background or have an explicit call to load the db
        self._run_data_pipeline()
        # Build open long event from trade_result
        return RemoveLiquidity(
            provider=to_checksum_address(tx_receipt.provider),
            lp_amount=tx_receipt.lp_amount,
            base_amount=tx_receipt.base_amount,
            share_price=tx_receipt.share_price,
            withdrawal_share_amount=tx_receipt.withdrawal_share_amount,
            lp_share_price=tx_receipt.lp_share_price,
        )

    def _redeem_withdraw_share(self, agent: HyperdriveAgent, shares: FixedPoint) -> RedeemWithdrawalShares:
        # Set the next action to open a long
        assert isinstance(agent.policy, InteractiveHyperdrivePolicy)
        agent.policy.set_next_action(HyperdriveActionType.REDEEM_WITHDRAW_SHARE, shares)
        # TODO expose async here to the caller eventually
        trade_results: list[TradeResult] = asyncio.run(
            async_execute_agent_trades(self.hyperdrive_interface, [agent], False)
        )
        tx_receipt = self._handle_trade_result(trade_results)
        # TODO running the data pipeline here may be slow, perhaps we should
        # do it in the background or have an explicit call to load the db
        self._run_data_pipeline()
        # Build open long event from trade_result
        return RedeemWithdrawalShares(
            provider=to_checksum_address(tx_receipt.provider),
            withdrawal_share_amount=tx_receipt.withdrawal_share_amount,
            base_amount=tx_receipt.base_amount,
            share_price=tx_receipt.share_price,
        )

    def _create_checkpoint(self, agent: HyperdriveAgent, checkpoint_time: int | None = None) -> CreateCheckpoint:
        # TODO need to figure out how to mint checkpoints on demand
        # https://github.com/delvtech/agent0/issues/1105
        raise NotImplementedError