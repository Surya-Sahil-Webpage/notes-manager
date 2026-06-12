# __init__.py
# Clean import syntax for routes:
#   from app.services import create_note, get_all_notes ...
# instead of:
#   from app.services.note import create_note ...

from .note import (
    create_note,
    get_all_notes,
    get_note_by_id,
    update_note,
    delete_note
)