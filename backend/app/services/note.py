# note.py (services)
# Contains all database operations for the Notes resource.
# Routes call these functions — they never interact with the session directly.
# This separation keeps routes thin and business logic testable in isolation.

from sqlalchemy.orm import Session
# Session → the type hint for the database session object
# Using it as a type hint (db: Session) enables IDE autocomplete
# and makes the function signature self-documenting

from app.models.note import Note
# Note → the SQLAlchemy model from Phase 4
# Every db.add(), db.query(), db.delete() operates on Note objects

from app.schemas.note import NoteCreate, NoteUpdate
# NoteCreate → Pydantic schema for incoming create data
# NoteUpdate → Pydantic schema for incoming update data
# We use these as type hints so Python knows what shape of data to expect


# ─── Create Note ──────────────────────────────────────────────────────────────
def create_note(db: Session, note_data: NoteCreate) -> Note:
    """
    Creates a new note in the database.
    Steps:
      1. Build a Note ORM object from the incoming Pydantic data
      2. Stage it with db.add()
      3. Commit the transaction to write it permanently
      4. Refresh to load DB-generated values (id, created_at, updated_at)
      5. Return the fully populated Note object
    """
    # Step 1: Create a Note ORM instance
    # note_data.model_dump() converts the Pydantic object → plain dict
    # { "title": "My Note", "content": "Some content" }
    # **note_data.model_dump() unpacks that dict as keyword arguments:
    # Note(title="My Note", content="Some content")
    db_note = Note(**note_data.model_dump())

    # Step 2: Stage the note
    # db.add() tells SQLAlchemy: "track this object, prepare to insert it"
    # At this point, NO SQL has been sent to PostgreSQL yet
    db.add(db_note)

    # Step 3: Commit the transaction
    # NOW the INSERT statement is sent to PostgreSQL and permanently written
    # If this fails (e.g. DB constraint violation), an exception is raised
    db.commit()

    # Step 4: Refresh the object
    # After commit, db_note is "expired" — SQLAlchemy clears its in-memory values
    # because the DB may have changed them (auto-generated id, timestamps)
    # db.refresh() sends a SELECT to reload the latest values from PostgreSQL
    # Without this: accessing db_note.id after commit → raises DetachedInstanceError
    db.refresh(db_note)

    # Step 5: Return the fully populated object
    # Now db_note.id, db_note.created_at, db_note.updated_at are all populated
    return db_note


# ─── Get All Notes ────────────────────────────────────────────────────────────
def get_all_notes(db: Session, skip: int = 0, limit: int = 100) -> list[Note]:
    """
    Retrieves all notes from the database, ordered newest first, with pagination.
    Returns a list of Note ORM objects (empty list if no notes exist).
    """
    return (
        db.query(Note)                          # SELECT * FROM notes
        .order_by(Note.created_at.desc())       # ORDER BY created_at DESC
        .offset(skip)                           # skip offset rows
        .limit(limit)                           # limit number of rows returned
        .all()                                  # fetch rows as a list
    )


# ─── Get Note By ID ───────────────────────────────────────────────────────────
def get_note_by_id(db: Session, note_id: int) -> Note | None:
    """
    Retrieves a single note by its primary key.
    Returns the Note object if found, None if not found.
    The route (Phase 7) is responsible for raising 404 if None is returned.
    """
    return (
        db.query(Note)                          # SELECT * FROM notes
        .filter(Note.id == note_id)             # WHERE id = note_id
        .first()                                # fetch first match or None
    )
    # Why .first() and not .one()?
    # .one() raises an exception if 0 or 2+ results found
    # .first() returns None if not found — cleaner for "does this exist?" checks


# ─── Update Note ──────────────────────────────────────────────────────────────
def update_note(db: Session, note_id: int, note_data: NoteUpdate) -> Note | None:
    """
    Updates an existing note's title and/or content.
    Supports partial updates — only fields provided in note_data are changed.
    Returns the updated Note, or None if the note doesn't exist.
    """
    # First: find the existing note
    db_note = get_note_by_id(db, note_id)

    # If note doesn't exist, return None
    # The route will convert this into a 404 response
    if db_note is None:
        return None

    # model_dump(exclude_unset=True) → only returns fields the client actually sent
    # If client sent { "title": "New Title" }, this gives { "title": "New Title" }
    # It does NOT include "content": None — so content stays unchanged in the DB
    # Without exclude_unset=True: content would be overwritten with None → data loss
    update_data = note_data.model_dump(exclude_unset=True)

    # Loop through provided fields and update the ORM object's attributes
    # setattr(db_note, "title", "New Title") is same as db_note.title = "New Title"
    for field, value in update_data.items():
        setattr(db_note, field, value)

    # Commit → writes the UPDATE statement to PostgreSQL
    db.commit()

    # Refresh → reloads updated_at (PostgreSQL just changed it via onupdate=func.now())
    db.refresh(db_note)

    return db_note


# ─── Delete Note ──────────────────────────────────────────────────────────────
def delete_note(db: Session, note_id: int) -> Note | None:
    """
    Deletes a note by ID.
    Returns the deleted Note object (so the route can confirm what was deleted),
    or None if the note doesn't exist.
    """
    # First: find the note
    db_note = get_note_by_id(db, note_id)

    # If not found, return None → route returns 404
    if db_note is None:
        return None

    # db.delete() marks the object for deletion
    # No SQL sent yet — just staged
    db.delete(db_note)

    # Commit → sends DELETE FROM notes WHERE id = ? to PostgreSQL
    db.commit()

    # No refresh needed — the object is deleted, nothing to reload
    # We return the object as it was before deletion
    # so the route can send back what was deleted if needed
    return db_note