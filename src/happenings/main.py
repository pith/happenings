"""
Main FastAPI application for the Happenings app.
"""

from fastapi import FastAPI

from happenings.infrastructure.persistence import Base, engine
from happenings.presentation import events_router, user_router

from .__about__ import __version__

# Create the database tables
# TODO: Move this to a separate migration script using Alembic or similar tool
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Happenings",
    description="An app to create and search for events in your neighborhood",
    version="0.0.1",
)

app.include_router(user_router, tags=["user"])
app.include_router(events_router, tags=["events"])


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "healthy", "version": __version__}
