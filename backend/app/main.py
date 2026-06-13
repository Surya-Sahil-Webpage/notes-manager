# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# CORSMiddleware → FastAPI middleware that adds CORS headers to every response
# This tells the browser: "yes, I allow requests from localhost:5173"

from app.routers import note as note_router

app = FastAPI(
    title="Notes Manager API",
    description="A simple CRUD API for managing notes",
    version="1.0.0"
)

# ─── CORS Middleware ───────────────────────────────────────────────────────────
# Must be added BEFORE routers are registered
# allow_origins → which frontend URLs are allowed to call this API
# allow_methods → which HTTP methods are permitted
# allow_headers → which request headers are permitted
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],       # GET, POST, PUT, DELETE
    allow_headers=["*"],       # Content-Type, Authorization, etc.
)

# ─── Register Routers ─────────────────────────────────────────────────────────
app.include_router(note_router.router)

# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"message": "Notes Manager API is running"}