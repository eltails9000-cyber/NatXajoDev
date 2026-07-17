import sqlite3
import logging
from datetime import datetime
from typing import Optional
from config import DATABASE_NAME

logger = logging.getLogger(__name__)


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    """Create all required tables if they don't exist."""
    with _get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bans (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                userid     TEXT    NOT NULL UNIQUE,
                reason     TEXT    NOT NULL,
                staff      TEXT    NOT NULL,
                created_at TEXT    NOT NULL
            )
            """
        )
        conn.commit()
    logger.info("Database initialized.")


def add_ban(userid: str, reason: str, staff: str) -> bool:
    """Insert a new ban record. Returns True on success, False if already banned."""
    try:
        with _get_connection() as conn:
            conn.execute(
                "INSERT INTO bans (userid, reason, staff, created_at) VALUES (?, ?, ?, ?)",
                (str(userid), reason, str(staff), datetime.utcnow().isoformat()),
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        logger.warning("Ban already exists for userid %s", userid)
        return False
    except sqlite3.Error as exc:
        logger.error("Error adding ban for userid %s: %s", userid, exc)
        return False


def remove_ban(userid: str) -> bool:
    """Remove a ban record. Returns True if a row was deleted."""
    try:
        with _get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM bans WHERE userid = ?", (str(userid),)
            )
            conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as exc:
        logger.error("Error removing ban for userid %s: %s", userid, exc)
        return False


def get_ban(userid: str) -> Optional[dict]:
    """Return the ban record for a user, or None if not found."""
    try:
        with _get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM bans WHERE userid = ?", (str(userid),)
            ).fetchone()
        return dict(row) if row else None
    except sqlite3.Error as exc:
        logger.error("Error fetching ban for userid %s: %s", userid, exc)
        return None


def is_banned(userid: str) -> bool:
    """Return True if the user has an active ban record."""
    return get_ban(userid) is not None
