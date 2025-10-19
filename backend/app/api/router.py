"""Root API router composition."""

from __future__ import annotations

from fastapi import APIRouter

from .routes import drafts, notes, organize, tags

router = APIRouter()
router.include_router(notes.router, prefix="/notes", tags=["notes"])
router.include_router(drafts.router, prefix="/drafts", tags=["drafts"])
router.include_router(tags.router, prefix="/tags", tags=["tags"])
router.include_router(organize.router, prefix="/organize", tags=["organize"])

__all__ = ["router"]
