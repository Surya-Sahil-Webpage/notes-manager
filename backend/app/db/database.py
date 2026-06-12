# database.py
# The foundation of all database operations in this project.
# Sets up three things: Engine, SessionLocal, and Base.

import os                               # Built-in — reads environment variables
from dotenv import load_dotenv          # Reads .env and loads vars into os.environ
from sqlalchemy import create_engine    # Creates the Engine (manages DB connections)
from sqlalchemy.orm import sessionmaker, declarative_base
# sessionmaker      → a factory that produces Session objects on demand
# declarative_base  → returns the Base class your models will inherit from

# ─── Load Environment Variables ───────────────────────────────────────────────
# Looks for .env in current working directory and injects each KEY=VALUE
# into os.environ so os.getenv() can read them at runtime
load_dotenv()

# Read DATABASE_URL from .env
# Value: postgresql://postgres:test1234!@localhost:5432/notes_manager
DATABASE_URL = os.getenv("DATABASE_URL")

# ─── Engine ───────────────────────────────────────────────────────────────────
# The Engine is SQLAlchemy's interface to PostgreSQL.
# It manages a "connection pool" — a fixed set of reusable open connections.
# Instead of opening a new TCP connection on every API request (expensive),
# the pool keeps connections alive and hands them out as needed.
#
# create_engine() does NOT connect immediately.
# The first actual connection happens lazily — when the first query runs.
engine = create_engine(DATABASE_URL)

# ─── SessionLocal ─────────────────────────────────────────────────────────────
# A Session is your workspace for one unit of work (one API request).
# You use it to:
#   - Add records:     session.add(note)
#   - Query records:   session.query(Note).all()
#   - Delete records:  session.delete(note)
#   - Save changes:    session.commit()   ← writes to DB permanently
#   - Undo changes:    session.rollback() ← cancels pending changes
#
# sessionmaker() returns a SESSION CLASS, not an instance.
# Each time you call SessionLocal(), you get a brand new Session object.
#
# autocommit=False → changes are NOT saved until you call session.commit()
# autoflush=False  → SQLAlchemy won't auto-send pending SQL before every query
# bind=engine      → tells sessions which engine (which database) to use
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ─── Base ─────────────────────────────────────────────────────────────────────
# Base is the parent class for all your SQLAlchemy models.
# When you define:
#   class Note(Base):
#       __tablename__ = "notes"
#
# SQLAlchemy registers that the Note class maps to the "notes" table.
# Base.metadata holds this registry — Alembic reads it to generate migrations.
Base = declarative_base()