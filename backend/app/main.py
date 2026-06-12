from fastapi import FastAPI

app = FastAPI(
    title="Notes Manager API",
    description="A simple CRUD API for managing notes",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Notes Manager API is running"}