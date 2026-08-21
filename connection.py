"""
database/connection.py

Sets up a single, reusable connection ("driver") to CognoDB.

CognoDB speaks openCypher over Bolt, so we connect to it using the
official Neo4j Python driver — no special CognoDB library needed.

This file only handles CONNECTING. The actual Cypher queries live in
database/queries.py (added in a later stage).
"""

import os
import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError

logger = logging.getLogger(__name__)

# This holds the single driver instance for the whole app.
# We create it once and reuse it, rather than opening a new
# connection for every request (that would be slow and wasteful).
_driver = None


def init_driver():
    """
    Create the Neo4j driver using credentials from environment variables.

    Call this once when the Flask app starts.

    Returns:
        True if the driver was created and the database responded,
        False if CognoDB could not be reached (app should still start,
        but should show a clear error state in the UI).
    """
    global _driver

    uri = os.environ.get("COGNODB_URI")
    username = os.environ.get("COGNODB_USERNAME")
    password = os.environ.get("COGNODB_PASSWORD")

    if not uri or not username or not password:
        logger.error(
            "Missing CognoDB environment variables. "
            "Check that COGNODB_URI, COGNODB_USERNAME and COGNODB_PASSWORD "
            "are set (copy .env.example to .env and fill them in)."
        )
        return False

    try:
        _driver = GraphDatabase.driver(uri, auth=(username, password))
        # verify_connectivity() actually pings the database. Without this,
        # GraphDatabase.driver() would succeed even if the URI is wrong,
        # because it doesn't connect until the first query.
        _driver.verify_connectivity()
        logger.info("Connected to CognoDB successfully.")
        return True

    except AuthError:
        logger.error("CognoDB rejected the username/password. Check COGNODB_PASSWORD.")
        _driver = None
        return False

    except ServiceUnavailable:
        logger.error("Could not reach CognoDB at the given URI. Check COGNODB_URI and that the instance is running.")
        _driver = None
        return False

    except Exception as e:
        logger.error(f"Unexpected error connecting to CognoDB: {e}")
        _driver = None
        return False


def get_driver():
    """
    Return the active driver, or None if we're not connected.

    Other files (queries.py, app.py) call this to get a handle
    they can run queries with. They must check for None before using it.
    """
    return _driver


def close_driver():
    """Cleanly close the connection. Call this when the app shuts down."""
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None
        logger.info("CognoDB connection closed.")