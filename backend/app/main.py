# main.py — Entry point of the FastAPI application
# FastAPI reads this file first when the server starts

from fastapi import FastAPI  # Import the FastAPI class — this IS your application

# Create the FastAPI application instance
# This object holds all your routes, middleware, and config
app = FastAPI(
    title="Notes Manager API",       # Shows up in Swagger UI
    description="A simple CRUD API for managing notes",
    version="1.0.0"
)

# A simple health-check route to confirm the server is running
# @app.get("/") means: when someone sends a GET request to "/", run this function
@app.get("/")
def root():
    # This function returns a JSON response automatically
    # FastAPI converts Python dicts → JSON for you
    return {"message": "Notes Manager API is running"}