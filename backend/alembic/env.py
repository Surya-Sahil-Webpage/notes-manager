# env.py
# Alembic's runtime configuration file.
# Runs every time you execute an alembic command.
# Two modes: online (with DB connection) and offline (generates raw SQL).
# We configure online mode only — standard for development.

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# ─── Load .env ────────────────────────────────────────────────────────────────
# Must happen before os.getenv() is called
load_dotenv()

# ─── Add backend/ to Python path ──────────────────────────────────────────────
# Alembic runs from the backend/ directory.
# Adding it to sys.path lets us import app modules (app.db, app.models, etc.)
# Without this: "ModuleNotFoundError: No module named 'app'"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ─── Import Base and all Models ───────────────────────────────────────────────
# Base.metadata is what Alembic compares against the current DB state
# to figure out what migrations need to be generated.
#
# CRITICAL: importing Note here ensures it's registered in Base.metadata.
# If you skip this import, Alembic won't detect the notes table → empty migration.
from app.db.database import Base
from app.models.note import Note  # noqa: F401 — imported for side effect (registration)

# ─── Alembic Config ───────────────────────────────────────────────────────────
# context.config gives access to alembic.ini settings
config = context.config

# Set up Python logging from alembic.ini's [loggers] section
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ─── Inject DATABASE_URL from .env ───────────────────────────────────────────
# Overrides the blank sqlalchemy.url in alembic.ini with the real value from .env
# This way credentials never live in alembic.ini (which IS committed to Git)
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# ─── Tell Alembic Which Metadata to Track ────────────────────────────────────
# target_metadata = Base.metadata means:
# "compare the current DB schema against all models registered in Base"
# This is what enables autogenerate — Alembic diffs model vs DB and writes SQL
target_metadata = Base.metadata


# ─── Online Migration (standard) ─────────────────────────────────────────────
def run_migrations_online():
    """
    Runs migrations with an active database connection.
    Standard mode for development and production.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # NullPool: don't reuse connections during migration
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


def run_migrations_offline():
    """
    Generates SQL scripts without a DB connection.
    Useful for reviewing changes before applying to production.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# ─── Run ──────────────────────────────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()