"""FastAPI application entrypoint for Bobo Notes."""

from __future__ import annotations

import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router as api_router

load_dotenv()

app = FastAPI(title="Bobo Notes API")

allowed_origins: List[str] = [
    os.getenv("FRONTEND_ORIGIN", "http://localhost:3000"),
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    """Simple health endpoint for uptime checks."""

    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
