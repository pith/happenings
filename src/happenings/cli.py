"""
Command-line interface for the Happenings app.
"""

import os

import uvicorn


def serve():
    """Run the FastAPI development server."""
    uvicorn.run(
        "happenings.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", default=8000)),
        reload=True,
    )


if __name__ == "__main__":
    serve()
