"""SQLAlchemy model and Pydantic schema for NoteLink."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID as UUIDType

from pydantic import BaseModel
from sqlalchemy import Enum as SAEnum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class NoteLinkType(str, Enum):
    EXPLICIT = "explicit"
    AI_INFERRED = "ai_inferred"


class NoteLink(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "note_links"

    source_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"), nullable=False
    )
    target_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"), nullable=False
    )
    link_type: Mapped[NoteLinkType] = mapped_column(
        SAEnum(NoteLinkType, name="note_link_type"), nullable=False
    )
    context_excerpt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    source: Mapped["Note"] = relationship(
        "Note", foreign_keys=[source_id], back_populates="note_links_out"
    )
    target: Mapped["Note"] = relationship(
        "Note", foreign_keys=[target_id], back_populates="note_links_in"
    )


class NoteLinkSchema(BaseModel):
    id: UUIDType
    source_id: UUIDType
    target_id: UUIDType
    link_type: NoteLinkType
    context_excerpt: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


__all__ = ["NoteLink", "NoteLinkSchema", "NoteLinkType"]
