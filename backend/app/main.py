# main.py
# Entry point of the FastAPI application.
# Registers all routers and any global middleware (CORS comes in Phase 15).

from fastapi import FastAPI
from app.routers import note as note_router
# Imports the routers/note.py module as note_router
# We use an alias to keep it clear: note_router.router is the APIRouter instance

app = FastAPI(
    title="Notes Manager API",
    description="A simple CRUD API for managing notes",
    version="1.0.0"
)

# ─── Register Routers ─────────────────────────────────────────────────────────
# include_router() attaches all routes defined in note_router.router to the app
# After this line, all 5 /notes endpoints are live and available
app.include_router(note_router.router)

# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"message": "Notes Manager API is running"}