# __init__.py
# Centralizes schema imports so routes can use clean import syntax:
#   from app.schemas import NoteCreate, NoteUpdate, NoteResponse
# instead of:
#   from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse

from .note import NoteCreate, NoteUpdate, NoteResponse