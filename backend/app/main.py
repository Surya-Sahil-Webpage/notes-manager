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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ← temporary wildcard to confirm CORS is the only issue
    allow_credentials=False,  # ← must be False when using wildcard
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(note_router.router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Notes Manager API is running"}