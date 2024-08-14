"""Script to format on-chain hyperdrive pool, config, and transaction data post-processing."""

from __future__ import annotations

import logging
import time
from typing import Callable

from eth_typing import ChecksumAddress
from sqlalchemy.orm import Session

from agent0.chainsync import PostgresConfig
from agent0.chainsync.analysis import db_to_analysis
from agent0.chainsync.db.base import initialize_session
from agent0.chainsync.db.hyperdrive import analysis_finalize_block, get_latest_ingestion_finalized_block_number
from agent0.ethpy.hyperdrive import HyperdriveReadInterface

_SLEEP_AMOUNT = 1


# TODO cleanup
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
def analyze_data(
    start_block: int = 0,
    interfaces: list[HyperdriveReadInterface] | None = None,
    rpc_uri: str | None = None,
    hyperdrive_addresses: list[ChecksumAddress] | dict[str, ChecksumAddress] | None = None,
    db_session: Session | None = None,
    postgres_config: PostgresConfig | None = None,
    exit_on_catch_up: bool = False,
    exit_callback_fn: Callable[[], bool] | None = None,
    suppress_logs: bool = False,
    calc_pnl: bool = True,
):
    """Execute the data acquisition pipeline.

    Arguments
    ---------
    start_block: int
        The starting block to filter the query on
    interfaces: list[HyperdriveReadInterface] | None, optional
        A collection of Hyperdrive interface objects, each connected to a pool.
        If not set, will initialize one based on rpc_uri and hyperdrive_address.
    rpc_uri: str, optional
        The URI for the web3 provider to initialize the interface with. Not used if an interface
        is provided.
    hyperdrive_addresses: list[ChecksumAddress] | dict[str, ChecksumAddress] | None, optional
        A collection of Hyperdrive address, each pointing to an initialized pool.
        Can also be the output of `get_hyperdrive_addresses_from_registry`, which is a
        dictionary keyed by a logical name and a value of a hyperdrive address.
        Not used if a list of interfaces is provided.
    db_session: Session | None
        Session object for connecting to db. If None, will initialize a new session based on
        .env.
    postgres_config: PostgresConfig | None = None,
        PostgresConfig for connecting to db. If none, will set from .env.
    exit_on_catch_up: bool
        If True, will exit after catching up to current block
    exit_callback_fn: Callable[[], bool] | None, optional
        A function that returns a boolean to call to determine if the script should exit.
        The function should return False if the script should continue, or True if the script should exit.
        Defaults to not set.
    suppress_logs: bool, optional
        If true, will suppress info logging from this function. Defaults to False.
    calc_pnl: bool
        Whether to calculate pnl. Defaults to True.
    """
    # TODO implement logger instead of global logging to suppress based on module name.

    ## Initialization
    if interfaces is None:
        if hyperdrive_addresses is None or rpc_uri is None:
            # TODO when we start deploying the registry, this case should look for existing
            # pools in the registry and use those.
            raise ValueError("hyperdrive_address and rpc_uri must be provided if not providing interface")

        if isinstance(hyperdrive_addresses, dict):
            # No need for the mapping here, `acquire_data` takes care of adding these mappings to the db
            hyperdrive_addresses = list(hyperdrive_addresses.values())

        interfaces = [
            HyperdriveReadInterface(hyperdrive_address, rpc_uri) for hyperdrive_address in hyperdrive_addresses
        ]

    # postgres session
    db_session_init = False
    if db_session is None:
        db_session_init = True
        db_session = initialize_session(postgres_config=postgres_config, ensure_database_created=True)

    curr_start_write_block = start_block
    # Main data loop
    # monitor for new blocks & add pool info per block
    if not suppress_logs:
        logging.info("Monitoring database for updates...")
    while True:
        latest_ingestion_block_number = get_latest_ingestion_finalized_block_number(db_session)
        # Only execute if we are on a new block
        if latest_ingestion_block_number < curr_start_write_block:
            exit_callable = False
            if exit_callback_fn is not None:
                exit_callable = exit_callback_fn()
            if exit_on_catch_up or exit_callable:
                break
            time.sleep(_SLEEP_AMOUNT)
            continue

        logging.info("Analyze data getting block %s", latest_ingestion_block_number)
        # FIXME
        print("Analyze data getting block %s", latest_ingestion_block_number)

        # Each table handles keeping track of appending to tables
        db_to_analysis(db_session, interfaces, calc_pnl)
        # Finalize the block
        analysis_finalize_block(db_session)
        curr_start_write_block = latest_ingestion_block_number + 1

    # Clean up resources on clean exit
    # If this function made the db session, we close it here
    if db_session_init:
        db_session.close()
