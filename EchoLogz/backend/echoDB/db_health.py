"""
DB health check utilities.

Used at app startup to verify that the real SQLite schema matches the
expected ORM models. If there is a mismatch, we raise an error with
clear instructions for teammates on how to fix their local DB.
"""

from backend.echoDB import db_session # , db_tables

from typing import Iterable
from sqlalchemy import inspect

def _get_column_names(table_name: str) -> set[str]:
    """Return the set of column names for a given table in the DB."""
    inspector = inspect(db_session.engine)
    cols = inspector.get_columns(table_name)
    return {col["name"] for col in cols}


def _check_table(
    table_name: str,
    expected_cols: Iterable[str],
    problems: list[str],
) -> None:
    """Compare actual vs expected column names for one table."""
    inspector = inspect(db_session.engine)

    if not inspector.has_table(table_name):
        problems.append(f"Missing table '{table_name}'.")
        return

    actual = _get_column_names(table_name)
    expected = set(expected_cols)

    missing = expected - actual
    extra = actual - expected

    if missing:
        problems.append(
            f"Table '{table_name}' is missing columns: {sorted(missing)}"
        )
    if extra:
        problems.append(
            f"Table '{table_name}' has unexpected columns: {sorted(extra)}"
        )


def assert_schema_matches() -> None:
    """
    Check that the live DB schema matches the expected ORM schema.

    If there is any mismatch, raise RuntimeError with a message that
    explains what to do (delete local DB and restart).
    """
    problems: list[str] = []

    # Users table
    _check_table(
        "users",
        expected_cols=("id", "email", "hashed_password", "is_verified"),
        problems=problems,
    )

    # Spotify accounts table
    _check_table(
        "spotify_accounts",
        expected_cols=(
            "id",
            "user_id",
            "spotify_user_id",
            "access_token",
            "refresh_token",
            "expires_at",
            "scope",
            "last_synced_at",
        ),
        problems=problems,
    )

    if not problems:
        return

    bullet_list = "\n".join(f"- {p}" for p in problems)

    fix_instructions = (
        "\n\n\nMESSAGE FROM ECHOLOGZ MANAGEMENT: \n---EchoLogz DB schema mismatch detected.\n"
        "Problems:\n"
        f"{bullet_list}\n\n"
        "How to fix (for all devs):\n"
        "  1) Stop the backend server: cntrl + c.\n"
        "  2) Delete your local DB file:\n"
        "       backend/data/echologz.db\n"
        "  3) Restart the backend (uvicorn) so echologz.db + tables are auto-generated from the ORM models.\n"
        "       uvicorn backend.main:app --reload\n"         
        "IMPORTANT: Do NOT manually create echologz.db — the backend will generate it automatically."
    )

    raise RuntimeError(fix_instructions)