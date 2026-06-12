# __init__.py
# Importing the Note model here serves one critical purpose:
# When Python loads this package, it executes this import,
# which causes SQLAlchemy to register Note in Base.metadata.
# Alembic imports this file during migrations — if Note isn't imported here,
# Alembic won't detect the table and won't generate a migration for it.

from .note import Note