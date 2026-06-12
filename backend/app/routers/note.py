# note.py (routers)
# Defines all HTTP endpoints for the Notes resource.
# Routes are intentionally thin — they validate input, call services, return output.
# No database logic lives here.

from fastapi import APIRouter, Depends, HTTPException, status
# APIRouter   → creates a modular group of routes (attached to app in main.py)
# Depends     → FastAPI's dependency injection — auto-calls get_db() per request
# HTTPException → raises HTTP error responses (404, 400, etc.) and stops execution
# status      → provides named HTTP status code constants (status.HTTP_404_NOT_FOUND)
#               using named constants is cleaner and self-documenting vs raw integers

from sqlalchemy.orm import Session
# Session → type hint for the injected database session

from app.db import get_db
# get_db → the dependency function from Phase 3
# FastAPI calls this before each route, injects the session, closes it after

from app.schemas import NoteCreate, NoteUpdate, NoteResponse
# NoteCreate   → validates POST request body
# NoteUpdate   → validates PUT request body
# NoteResponse → shapes every response sent back to the frontend

from app import services
# services → the package from Phase 6
# We import the package itself and call services.create_note(...)
# This makes it explicit WHERE each function comes from


# ─── Router Instance ──────────────────────────────────────────────────────────
# prefix="/notes" → every route defined here automatically starts with /notes
# tags=["Notes"]  → groups these endpoints under "Notes" in Swagger UI
router = APIRouter(prefix="/notes", tags=["Notes"])


# ─── POST /notes ──────────────────────────────────────────────────────────────
# Creates a new note
# status_code=201 → HTTP 201 Created (more accurate than 200 for resource creation)
# response_model=NoteResponse → FastAPI uses this to serialize the return value
#   it filters out any fields not in NoteResponse and validates the output shape
@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_data: NoteCreate,          # FastAPI reads + validates the JSON request body
    db: Session = Depends(get_db)   # FastAPI injects the DB session automatically
):
    """Create a new note."""
    # Call the service — all DB logic lives there
    return services.create_note(db=db, note_data=note_data)


# ─── GET /notes ───────────────────────────────────────────────────────────────
# Returns all notes as a list
# list[NoteResponse] → response is an array of NoteResponse objects
@router.get("/", response_model=list[NoteResponse], status_code=status.HTTP_200_OK)
def get_all_notes(
    db: Session = Depends(get_db)
):
    """Retrieve all notes."""
    return services.get_all_notes(db=db)


# ─── GET /notes/{note_id} ─────────────────────────────────────────────────────
# Returns a single note by ID
# {note_id} → path parameter, FastAPI extracts it from the URL and passes it in
# FastAPI automatically validates it's an integer — /notes/abc returns 422
@router.get("/{note_id}", response_model=NoteResponse, status_code=status.HTTP_200_OK)
def get_note(
    note_id: int,                   # extracted from URL path automatically
    db: Session = Depends(get_db)
):
    """Retrieve a single note by ID."""
    note = services.get_note_by_id(db=db, note_id=note_id)

    # Service returns None if note doesn't exist
    # We convert that into a proper 404 HTTP response
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )

    return note


# ─── PUT /notes/{note_id} ─────────────────────────────────────────────────────
# Updates an existing note (partial update supported)
@router.put("/{note_id}", response_model=NoteResponse, status_code=status.HTTP_200_OK)
def update_note(
    note_id: int,
    note_data: NoteUpdate,          # validates the update request body
    db: Session = Depends(get_db)
):
    """Update an existing note by ID."""
    note = services.update_note(db=db, note_id=note_id, note_data=note_data)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )

    return note


# ─── DELETE /notes/{note_id} ──────────────────────────────────────────────────
# Deletes a note by ID
# Returns 200 with a confirmation message (some APIs return 204 No Content)
# We return 200 + message so the frontend gets explicit confirmation
@router.delete("/{note_id}", status_code=status.HTTP_200_OK)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    """Delete a note by ID."""
    note = services.delete_note(db=db, note_id=note_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )

    # Return confirmation — what was deleted and its id
    return {"message": f"Note with id {note_id} deleted successfully"}