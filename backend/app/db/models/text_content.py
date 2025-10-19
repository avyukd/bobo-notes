"""SQLAlchemy model and Pydantic schema for TextContent."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType

from pydantic import BaseModel
from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class TextContent(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "text_contents"

    note_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    note: Mapped["Note"] = relationship("Note", back_populates="text_content")


class TextContentSchema(BaseModel):
    id: UUIDType
    note_id: UUIDType
    body: str
    embedding: Optional[dict]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


__all__ = ["TextContent", "TextContentSchema"]
