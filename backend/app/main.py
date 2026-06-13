# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers import note as note_router

load_dotenv()

app = FastAPI(
    title="Notes Manager API",
    description="A simple CRUD API for managing notes",
    version="1.0.0"
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
# Read allowed origins from environment variable
# Local: CORS_ORIGINS=http://localhost:5173
# Production: CORS_ORIGINS=https://notes-manager.vercel.app
# os.getenv returns a string — split by comma to support multiple origins
cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173"   # default for local development
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(note_router.router)

# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"message": "Notes Manager API is running"}