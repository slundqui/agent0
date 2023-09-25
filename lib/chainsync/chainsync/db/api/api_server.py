"""A simple Flask server to run python scripts."""
from __future__ import annotations

import logging

from chainsync.db.base import add_user_map, close_session, initialize_session
from chainsync.db.hyperdrive import get_current_wallet
from flask import Flask, jsonify, request
from flask_expects_json import expects_json

app = Flask(__name__)


register_agents_json_schema = {
    "type": "object",
    "properties": {"wallet_addrs": {"type": "array", "items": {"type": "string"}}, "username": {"type": "string"}},
    "required": ["wallet_addrs", "username"],
}


@app.route("/register_agents", methods=["POST"])
@expects_json(register_agents_json_schema)
def register_agents():
    """Registers a list of wallet addresses to a username via post request"""
    # TODO: validate the json
    data = request.json
    if data is not None:
        wallet_addrs: list[str] = data["wallet_addrs"]
        username: str = data["username"]
    else:
        return jsonify({"data": data, "error": "request.json is None"}), 500

    # initialize the postgres session
    # This function gets env variables for db credentials
    session = initialize_session()
    try:
        add_user_map(username, wallet_addrs, session)
        logging.debug("Registered wallet_addrs=%s to username=%s}", wallet_addrs, username)
        out = (jsonify({"data": data, "error": ""}), 200)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        # Ignoring broad exception, since we're simply printing out error and returning to client
        out = (jsonify({"data": data, "error": str(exc)}), 500)

    close_session(session)
    return out


balance_of_json_schema = {
    "type": "object",
    "properties": {"wallet_addrs": {"type": "array", "items": {"type": "string"}}},
    "required": ["wallet_addrs"],
}


@app.route("/balance_of", methods=["POST"])
@expects_json(balance_of_json_schema)
def balance_of():
    """Retrieves the balance of a given wallet address from the db.
    Note that this only takes into account token differences from opening and closing
    longs and shorts, not any transfer events between wallets.
    """
    # TODO: validate the json
    data = request.json
    if data is not None:
        wallet_addrs: list[str] = data["wallet_addrs"]
    else:
        return jsonify({"data": data, "error": "request.json is None"}), 500

    # initialize the postgres session
    # This function gets env variables for db credentials
    session = initialize_session()
    try:
        logging.debug("Querying wallet_addrs=%s for balances}", wallet_addrs)
        current_wallet = get_current_wallet(session, wallet_address=wallet_addrs, coerce_float=False)
        # Cast decimal to string, then convert to json and return
        data = current_wallet.astype(str).to_json()

        # Convert dataframe to json
        out = (jsonify({"data": data, "error": ""}), 200)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        # Ignoring broad exception, since we're simply printing out error and returning to client
        out = (jsonify({"data": data, "error": str(exc)}), 500)

    close_session(session)
    return out


def launch_flask(host: str = "0.0.0.0", port: int = 5002):
    """Launches the flask server

    Arguments
    ---------
    db_session: Session | None
        Session object for connecting to db. If None, will initialize a new session based on
        postgres.env.
    """
    app.run(host=host, port=port)