"""Request payload schemas for API routes."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from ...db.models import NoteContentType


class NoteCreate(BaseModel):
    title: str = Field(..., max_length=255)
    content_type: NoteContentType
    body: Optional[str] = None


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    content_type: Optional[NoteContentType] = None
    archived: Optional[bool] = None
    body: Optional[str] = None

    class Config:
        extra = "forbid"


class DraftCreate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

    class Config:
        extra = "forbid"
