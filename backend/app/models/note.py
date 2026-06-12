# note.py
# Defines the Note SQLAlchemy model.
# This class is the Python representation of the "notes" table in PostgreSQL.
# SQLAlchemy reads this and knows exactly what columns the table has.

from sqlalchemy import Column, Integer, String, Text, DateTime
# Column    → marks a class attribute as a database column
# Integer   → maps to PostgreSQL INTEGER — whole numbers (1, 2, 3)
# String    → maps to PostgreSQL VARCHAR — short text with a length limit
# Text      → maps to PostgreSQL TEXT — long text with no length limit
# DateTime  → maps to PostgreSQL TIMESTAMP — date and time values

from sqlalchemy.sql import func
# func      → gives access to SQL functions
# func.now() → calls PostgreSQL's NOW() function which returns current timestamp

from app.db.database import Base
# Base      → the parent class from Phase 3
# Inheriting from Base registers this model in SQLAlchemy's metadata registry
# Without this, Alembic won't know this table exists


class Note(Base):
    # __tablename__ tells SQLAlchemy what to name the table in PostgreSQL
    # Convention: class names are singular (Note), table names are plural (notes)
    __tablename__ = "notes"

    # ─── Primary Key ──────────────────────────────────────────────────────────
    # Every table needs a primary key — a unique identifier for each row
    # Integer + primary_key=True → PostgreSQL creates a SERIAL (auto-increment)
    # You never set this manually — the DB assigns it automatically: 1, 2, 3...
    id = Column(Integer, primary_key=True, index=True)
    # index=True → creates a database index on this column
    # An index makes lookups by id extremely fast (like a book's index)

    # ─── Title ────────────────────────────────────────────────────────────────
    # String(255) → VARCHAR(255) in PostgreSQL — max 255 characters
    # nullable=False → this column is required, cannot be empty/NULL
    title = Column(String(255), nullable=False)

    # ─── Content ──────────────────────────────────────────────────────────────
    # Text → PostgreSQL TEXT — no character limit, stores large bodies of text
    # nullable=False → content is required, every note must have it
    content = Column(Text, nullable=False)

    # ─── Timestamps ───────────────────────────────────────────────────────────
    # created_at → automatically set to current time when a note is first created
    # server_default=func.now() means PostgreSQL itself sets this value
    # using its NOW() function — not Python, not your code — the database does it
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # updated_at → automatically updates every time this record is modified
    # onupdate=func.now() tells SQLAlchemy: whenever this row is updated,
    # re-run func.now() and store the new timestamp in this column
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # set on creation
        onupdate=func.now()         # update on every modification
    )