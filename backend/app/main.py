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
    allow_origins=[
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "https://notes-manager-eight-topaz.vercel.app,http://localhost:5173,http://127.0.0.1:5173").split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(note_router.router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Notes Manager API is running"}