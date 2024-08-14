"""Defines the interactive hyperdrive class that encapsulates a hyperdrive pool."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Sequence

import nest_asyncio
import pandas as pd
from eth_typing import ChecksumAddress

from agent0.chainsync.analysis import fill_pnl_values
from agent0.chainsync.db.hyperdrive import (
    add_hyperdrive_addr_to_name,
    get_checkpoint_info,
    get_pool_config,
    get_pool_info,
    get_position_snapshot,
    get_total_pnl_over_time,
    get_trade_events,
)
from agent0.ethpy.hyperdrive import (
    HyperdriveReadWriteInterface,
    get_hyperdrive_addresses_from_registry,
    get_hyperdrive_name,
)

if TYPE_CHECKING:
    from .chain import Chain

# In order to support both scripts and jupyter notebooks with underlying async functions,
# we use the nest_asyncio package so that we can execute asyncio.run within a running event loop.
# TODO: nest_asyncio may cause compatibility issues with other libraries.
# Also, Jupyter and ASYNC compatibility might be improved, removing the need for this.
# See https://github.com/python/cpython/issues/66435.
nest_asyncio.apply()


class Hyperdrive:
    """Interactive Hyperdrive class that supports connecting to an existing hyperdrive deployment."""

    # Lots of config
    # pylint: disable=too-many-instance-attributes
    @dataclass(kw_only=True)
    class Config:
        """The configuration for the interactive hyperdrive class."""

    @classmethod
    def get_hyperdrive_addresses_from_registry(
        cls,
        chain: Chain,
        registry_address: str,
    ) -> dict[str, ChecksumAddress]:
        """Gather deployed Hyperdrive pool addresses.

        Arguments
        ---------
        chain: Chain
            The Chain object connected to a chain.
        registry_address: str
            The address of the Hyperdrive factory contract.

        Returns
        -------
        dict[str, ChecksumAddress]
            A dictionary keyed by the pool's name, valued by the pool's address
        """
        # pylint: disable=protected-access
        return get_hyperdrive_addresses_from_registry(registry_address, chain._web3)

    @classmethod
    def get_hyperdrive_pools_from_registry(
        cls,
        chain: Chain,
        registry_address: str,
    ) -> Sequence[Hyperdrive]:
        """Gather deployed Hyperdrive pool addresses.

        Arguments
        ---------
        chain: Chain
            The Chain object connected to a chain.
        registry_address: str
            The address of the Hyperdrive registry contract.

        Returns
        -------
        Sequence[Hyperdrive]
            The hyperdrive objects for all registered pools
        """

        # Explicit type check to ensure chain is not LocalChain
        if chain.is_local_chain:
            raise TypeError(
                "Cannot use `Hyperdrive` function on `LocalChain` object. "
                "Use `LocalHyperdrive.get_hyperdrive_pools_from_registry` instead."
            )

        hyperdrive_addresses = cls.get_hyperdrive_addresses_from_registry(chain, registry_address)
        if len(hyperdrive_addresses) == 0:
            raise ValueError("Registry does not have any hyperdrive pools registered.")
        # Generate hyperdrive pool objects here
        registered_pools = []
        for hyperdrive_name, hyperdrive_address in hyperdrive_addresses.items():
            registered_pools.append(Hyperdrive(chain, hyperdrive_address, name=hyperdrive_name))

        return registered_pools

    # Pretty print for this class
    def __str__(self) -> str:
        return f"Hyperdrive Pool {self.name} at chain address {self.hyperdrive_address}"

    def __repr__(self) -> str:
        return "<" + str(self) + ">"

    def _initialize(self, chain: Chain, hyperdrive_address: ChecksumAddress, name: str | None):
        self.chain = chain

        self.interface = HyperdriveReadWriteInterface(
            hyperdrive_address,
            rpc_uri=chain.rpc_uri,
            web3=chain._web3,  # pylint: disable=protected-access
            txn_receipt_timeout=self.chain.config.txn_receipt_timeout,
            txn_signature=self.chain.config.txn_signature,
        )

        # Register the username if it was provided
        if name is None:
            # Build the name in this case
            name = get_hyperdrive_name(
                self.hyperdrive_address,
                self.chain._web3,  # pylint: disable=protected-access
            )

        add_hyperdrive_addr_to_name(name, self.hyperdrive_address, self.chain.db_session)
        self.name = name

        # Set the crash report's additional information from the chain.
        self._crash_report_additional_info = {}
        if self.chain.config.crash_report_additional_info is not None:
            self._crash_report_additional_info.update(self.chain.config.crash_report_additional_info)

    def __init__(
        self,
        chain: Chain,
        hyperdrive_address: ChecksumAddress,
        config: Config | None = None,
        name: str | None = None,
    ):
        """Initialize the interactive hyperdrive class.

        Arguments
        ---------
        chain: Chain
            The chain to interact with
        hyperdrive_address: ChecksumAddress
            The address of the hyperdrive contract
        config: Config | None
            The configuration for the interactive hyperdrive class
        name: str | None, optional
            The logical name of the pool.
        """
        if config is None:
            self.config = self.Config()
        else:
            self.config = config

        # Since the hyperdrive objects manage data ingestion into the singular database
        # held by the chain object, we want to ensure that we dont mix and match
        # local vs non-local hyperdrive objects. Hence, we ensure that any hyperdrive
        # objects must come from a base Chain object and not a LocalChain.
        if chain.is_local_chain:
            raise TypeError("The chain parameter must be a Chain object, not a LocalChain.")

        self._initialize(chain, hyperdrive_address, name)

    ### Database methods
    # These methods expose the underlying chainsync getter methods with minimal processing
    # TODO expand in docstrings the columns of the output dataframe

    def get_pool_config(self, coerce_float: bool = False) -> pd.Series:
        """Get the pool config and returns as a pandas series.

        Arguments
        ---------
        coerce_float: bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Series
            A pandas series that consists of the deployed pool config.
        """
        # Underlying function returns a dataframe, but this is assuming there's a single
        # pool config for this object.
        pool_config = get_pool_config(self.chain.db_session, coerce_float=coerce_float)
        if len(pool_config) == 0:
            raise ValueError("Pool config doesn't exist in the db.")
        return pool_config.iloc[0]

    def get_pool_info(self, coerce_float: bool = False) -> pd.DataFrame:
        """Get the pool info (and additional info) per block and returns as a pandas dataframe.

        Arguments
        ---------
        coerce_float: bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Dataframe
            A pandas dataframe that consists of the pool info per block.
        """
        self.chain.wait_for_ingestion_pipeline()
        pool_info = get_pool_info(self.chain.db_session, coerce_float=coerce_float).drop("id", axis=1)
        return pool_info

    def get_checkpoint_info(self, coerce_float: bool = False) -> pd.DataFrame:
        """Get the previous checkpoint infos per block and returns as a pandas dataframe.

        Arguments
        ---------
        coerce_float: bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Dataframe
            A pandas dataframe that consists of previous checkpoints made on this pool.
        """
        self.chain.wait_for_ingestion_pipeline()
        return get_checkpoint_info(
            self.chain.db_session, hyperdrive_address=self.hyperdrive_address, coerce_float=coerce_float
        )

    def get_positions(
        self,
        show_closed_positions: bool = False,
        calc_pnl: bool = False,
        coerce_float: bool = False,
    ) -> pd.DataFrame:
        """Gets all current positions of this pool and their corresponding pnl
        and returns as a pandas dataframe.

        This function only exists in local hyperdrive as only sim pool keeps track
        of all positions of all wallets.

        Arguments
        ---------
        show_closed_positions: bool, optional
            Whether to show positions closed positions (i.e., positions with zero balance). Defaults to False.
            When False, will only return currently open positions. Useful for gathering currently open positions.
            When True, will also return any closed positions. Useful for calculating overall pnl of all positions.
            Defaults to False.
        calc_pnl: bool, optional
            If the chain config's `calc_pnl` flag is False, passing in `calc_pnl=True` to this function allows for
            a one-off pnl calculation for the current positions. Ignored if the chain's `calc_pnl` flag is set to True,
            as every position snapshot will return pnl information.
        coerce_float: bool
            If True, will coerce underlying Decimals to floats.
            Defaults to False.

        Returns
        -------
        pd.Dataframe
            A dataframe consisting of currently open positions and their corresponding pnl.
        """
        self.chain.wait_for_analysis_pipeline()
        position_snapshot = get_position_snapshot(
            self.chain.db_session,
            hyperdrive_address=self.interface.hyperdrive_address,
            latest_entry=True,
            coerce_float=coerce_float,
        ).drop("id", axis=1)
        if not show_closed_positions:
            position_snapshot = position_snapshot[position_snapshot["token_balance"] != 0].reset_index(drop=True)

        # If the config's calc_pnl is not set, but we pass in `calc_pnl = True` to this function,
        # we do a one off calculation to get the pnl here.
        if not self.chain.config.calc_pnl and calc_pnl:
            position_snapshot = fill_pnl_values(
                position_snapshot,
                self.chain.db_session,
                self.interface,
                coerce_float=coerce_float,
            )

        # Add usernames
        position_snapshot = self.chain._add_username_to_dataframe(position_snapshot, "wallet_address")
        # Add logical name for pool
        position_snapshot = self.chain._add_hyperdrive_name_to_dataframe(position_snapshot, "hyperdrive_address")
        return position_snapshot

    def get_trade_events(self, all_token_deltas: bool = False, coerce_float: bool = False) -> pd.DataFrame:
        """Gets the ticker history of all trades and the corresponding token deltas for each trade.

        This function is not implemented for remote hyperdrive, as gathering this data
        is expensive. In the future, we can explicitly make this call gather data from
        the remote chain.

        Arguments
        ---------
        all_token_deltas: bool
            When removing liquidity that results in withdrawal shares, the events table returns
            two entries for this transaction to keep track of token deltas (one for lp tokens and
            one for withdrawal shares). If this flag is true, will return all entries in the table,
            which is useful for calculating token positions. If false, will drop the duplicate
            withdrawal share entry (useful for returning a ticker).
        coerce_float: bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Dataframe
            A dataframe of trade events.
        """
        # pylint: disable=protected-access

        self.chain.wait_for_ingestion_pipeline()
        out = get_trade_events(
            self.chain.db_session,
            hyperdrive_address=self.interface.hyperdrive_address,
            all_token_deltas=all_token_deltas,
            coerce_float=coerce_float,
        ).drop("id", axis=1)
        out = self.chain._add_username_to_dataframe(out, "wallet_address")
        out = self.chain._add_hyperdrive_name_to_dataframe(out, "hyperdrive_address")
        return out

    def get_historical_positions(self, coerce_float: bool = False) -> pd.DataFrame:
        """Gets the history of all positions over time and their corresponding pnl
        and returns as a pandas dataframe.

        This function is not implemented for remote hyperdrive, as gathering this data
        is expensive. In the future, we can explicitly make this call gather data from
        the remote chain.

        Arguments
        ---------
        coerce_float: bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Dataframe
            A dataframe consisting of positions over time and their corresponding pnl.
        """
        self.chain.wait_for_analysis_pipeline()
        # TODO add logical name for pool
        position_snapshot = get_position_snapshot(
            self.chain.db_session, hyperdrive_address=self.interface.hyperdrive_address, coerce_float=coerce_float
        ).drop("id", axis=1)
        # Add usernames
        position_snapshot = self.chain._add_username_to_dataframe(position_snapshot, "wallet_address")
        position_snapshot = self.chain._add_hyperdrive_name_to_dataframe(position_snapshot, "hyperdrive_address")
        return position_snapshot

    def get_historical_pnl(self, coerce_float: bool = False) -> pd.DataFrame:
        """Gets total pnl for each wallet for each block, aggregated across all open positions.

        This function is not implemented for remote hyperdrive, as gathering this data
        is expensive. In the future, we can explicitly make this call gather data from
        the remote chain.

        Arguments
        ---------
        coerce_float: bool
            If True, will coerce underlying Decimals to floats.

        Returns
        -------
        pd.Dataframe
            A dataframe of aggregated wallet pnl per block
        """
        out = get_total_pnl_over_time(self.chain.db_session, coerce_float=coerce_float)
        out = self.chain._add_username_to_dataframe(out, "wallet_address")
        return out

    @property
    def hyperdrive_address(self) -> ChecksumAddress:
        """Returns the hyperdrive addresses for this pool.

        Returns
        -------
        ChecksumAddress
            The hyperdrive addresses for this pool
        """
        # pylint: disable=protected-access
        return self.interface.hyperdrive_address
