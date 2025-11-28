"""
----------------------------------------------------------------------------
MODULE: Database ORM Models: DB Blueprint - ORM table models (db_tables.py)
----------------------------------------------------------------------------

This module defines the database schema for EchoLogz using SQLAlchemy ORM. 
Each model/class represents a table in the database and maps Python objects 
to relational database records.

NOTE: SQAlchemy ORM models (Object-Relational Mapping models) are Python classes that represent tables in a relational database. Each class corresponds to one table, and each class attribute corresponds to a database column. The ORM automatically translates between Python objects and SQL queries, so you can work with database rows using normal Python code instead of writing raw SQL statements. 
NOTE: ORM models are *pythonic schemas* that are also mapped directly to actual database tables — meaning they act as both the blueprint and the concrete table representation at once.

Responsibilities:
- Defines table structures and their columns (schemas).
- Maps Python classes to relational database tables using SQLAlchemy ORM.
- Establishes relationships (foreign keys, joins) between tables.
- Inherits from Base (provided by db_session.py) to register models with SQLAlchemy.
────────────────────────────────────────────
Modules using db_tables.py:
- db_crud.py
- db_session.py

INTERNAL IMPORTS:
- db_session.py     -> Provides the SQLAlchemy Base class used for model inheritance.

EXTERNAL IMPORTS:
- SQAlchemy
────────────────────────────────────────────
NOTE: Spotify Developer Terms = “Except as otherwise set out in these Developer Terms, you may not store, aggregate or create compilations or databases of Spotify Content, other than as strictly necessary to operate your SDA.”
WORK AROUND: Store Track IDs + URIs (this is ok)
        
"""

# INTERNAL IMPORTS: 
from backend.echoDB.db_session import Base

# EXTERNAL IMPORTS:
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


# =========================================================================
#      EchoLogz User Table
# =========================================================================

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    # username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Link to SpotifyAccount rows
    spotify_accounts = relationship(
        "SpotifyAccount",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

# TRANSLATES TO:
# CREATE TABLE users (
#     id INTEGER PRIMARY KEY,
#     username VARCHAR NOT NULL UNIQUE,
#     email VARCHAR NOT NULL UNIQUE,
#     hashed_password VARCHAR NOT NULL
# ); # but then also connected directly to the actual table -- not just the schema

""" 
EchoLogz Spotify Data Rules
---------------------------
What EchoLogz *can* store:
    - Spotify user ID
    - Access token
    - Refresh token
    - Token expiration time
    - Granted scopes
    - Timestamp of last Spotify sync
    - Small derived data (like numeric taste vectors)
    - Track IDs / URIs, Artist IDs, Playlist IDs (possible workaround for some ideas?)

What EchoLogz *cannot* store:
    - Spotify passwords
    - OAuth authorization codes after use
    - Raw audio files
    - Full listening history dumps
    - Entire playlists or large metadata snapshots
    - Any data beyond what is required for EchoLogz features
    - Any Spotify-derived data after the user disconnects

Required behavior when using Spotify data:
    - Use refresh tokens to get new access tokens when needed.
    - Only call Spotify APIs inside the scopes the user approved.
    - Generate compact numeric vectors for compatibility instead of storing full metadata.
    - Never log tokens or user IDs in plain text.
    - Never expose tokens to the front-end.

Required behavior on disconnect/delete:
    - Remove the SpotifyAccount row for the user.
    - Delete all Spotify-derived cached vectors or metadata.
"""

# =========================================================================
#      Spotify User Table
# =========================================================================
class SpotifyAccount(Base):
    __tablename__ = "spotify_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(                                             # FK to EchoLogz users table
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    spotify_user_id = Column(String, nullable=False, index=True)   # Spotify’s stable user identifier
    access_token = Column(String, nullable=False)                  # OAuth2 token bundle
    refresh_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)                  # When the access token expires (UTC)
    scope = Column(String, nullable=True)                          # Optional: space-separated scopes requested
    last_synced_at = Column(DateTime, nullable=True, default=None) # Bookkeeping: last time we pulled data from Spotify
    user = relationship(                                           # ORM relationship back to User
        "User",
        back_populates="spotify_accounts",
    )