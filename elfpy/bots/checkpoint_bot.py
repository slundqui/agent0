"""A checkpoint bot for Hyperdrive"""
from __future__ import annotations

import datetime
import logging
import os
import time
from dotenv import load_dotenv

from web3.contract.contract import Contract

from elfpy import eth, hyperdrive_interface
from elfpy.agents.agent import Agent
from elfpy.eth.accounts.eth_account import EthAccount
from elfpy.eth.rpc_interface import set_anvil_account_balance
from elfpy.eth.transactions import smart_contract_read, smart_contract_transact
from elfpy.utils import logs
from elfpy.bots.environment_config import EnvironmentConfig
from elfpy.hyperdrive_interface.hyperdrive_interface import get_hyperdrive_config

# The portion of the checkpoint that the bot will wait before attempting to
# mint a new checkpoint.
CHECKPOINT_WAITING_PERIOD = 0.5


def get_config() -> EnvironmentConfig:
    """Gets the Hyperdrive configuration."""

    # Load some configuration variables from the environment.
    load_dotenv()
    artifacts_url = os.environ.get("ARTIFACTS_URL")
    if artifacts_url is None:
        raise ValueError("ARTIFACTS_URL environment variable must be set")
    rpc_url = os.environ.get("RPC_URL")
    if rpc_url is None:
        raise ValueError("RPC_URL environment variable must be set")

    # The configuration for the checkpoint bot halts on errors and logs to stdout.
    return EnvironmentConfig(
        # Networking
        artifacts_url=artifacts_url,
        rpc_url=rpc_url,
        # Errors
        halt_on_errors=True,
        # Logging
        log_stdout=True,
        log_level=logging.INFO,
    )


def does_checkpoint_exist(hyperdrive: Contract, checkpoint_time: int) -> bool:
    """Checks whether or not a given checkpoint exists."""

    return smart_contract_read(hyperdrive, "getCheckpoint", int(checkpoint_time))["sharePrice"] > 0


def main() -> None:
    """Runs the checkpoint bot."""

    # Get the configuration and initialize the web3 provider.
    config = get_config()
    web3 = eth.web3_setup.initialize_web3_with_http_provider(config.rpc_url, reset_provider=False)

    # Setup logging
    logs.setup_logging(
        log_filename=config.log_filename,
        max_bytes=config.max_bytes,
        log_level=config.log_level,
        delete_previous_logs=config.delete_previous_logs,
        log_stdout=config.log_stdout,
        log_format_string=config.log_formatter,
    )

    # Fund the checkpoint sender with some ETH.
    balance = int(100e18)
    sender = EthAccount(agent=Agent(wallet_address=0))
    set_anvil_account_balance(web3, sender.account.address, balance)
    logging.info("Successfully funded the sender=%s.", sender.account.address)

    # Get the Hyperdrive contract.
    hyperdrive_abis = eth.abi.load_all_abis(config.build_folder)
    addresses = hyperdrive_interface.fetch_hyperdrive_address_from_url(
        os.path.join(config.artifacts_url, "addresses.json")
    )
    hyperdrive: Contract = web3.eth.contract(
        abi=hyperdrive_abis[config.hyperdrive_abi],
        address=web3.to_checksum_address(addresses.mock_hyperdrive),
    )

    # Run the checkpoint bot. This bot will attempt to mint a new checkpoint
    # every checkpoint after a waiting period. It will poll very infrequently
    # to reduce the probability of needing to mint a checkpoint.
    config = get_hyperdrive_config(hyperdrive)
    checkpoint_duration = config["checkpointDuration"]
    while True:
        # Get the latest block time and check to see if a new checkpoint should
        # be minted. This bot waits for a portion of the checkpoint to reduce
        # the probability of needing a checkpoint. After the waiting period,
        # the bot will attempt to mint a checkpoint.
        latest_block = web3.eth.get_block("latest")
        timestamp = latest_block.get("timestamp", None)
        if timestamp is None:
            raise AssertionError(f"{latest_block=} has no timestamp")
        checkpoint_portion_elapsed = timestamp % checkpoint_duration
        checkpoint_time = timestamp - timestamp % checkpoint_duration
        if checkpoint_portion_elapsed >= CHECKPOINT_WAITING_PERIOD * checkpoint_duration and not does_checkpoint_exist(
            hyperdrive, checkpoint_time
        ):
            logging.info("Submitting a checkpoint for checkpointTime=%s...", checkpoint_time)
            # TODO: We will run into issues with the gas price being too low
            # with testnets and mainnet. When we get closer to production, we
            # will need to make this more robust so that we retry this
            # transaction if the transaction gets stuck.
            receipt = smart_contract_transact(
                web3,
                hyperdrive,
                sender,
                "checkpoint",
                (checkpoint_time),
            )
            logging.info(
                "Checkpoint successfully mined with receipt=%s",
                receipt["transactionHash"].hex(),
            )

        # Sleep for enough time that the block timestamp would have advanced
        # far enough to consider minting a new checkpoint.
        if checkpoint_portion_elapsed >= CHECKPOINT_WAITING_PERIOD * checkpoint_duration:
            sleep_duration = checkpoint_duration * (1 + CHECKPOINT_WAITING_PERIOD) - checkpoint_portion_elapsed
        else:
            sleep_duration = checkpoint_duration * CHECKPOINT_WAITING_PERIOD - checkpoint_portion_elapsed
        logging.info(
            "Current time is %s. Sleeping for %s seconds ...",
            datetime.datetime.fromtimestamp(timestamp),
            sleep_duration,
        )
        time.sleep(sleep_duration)


# Run the checkpoint bot.
main()