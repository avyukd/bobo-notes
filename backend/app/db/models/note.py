"""SQLAlchemy model and Pydantic schema for Note."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID as UUIDType

from pydantic import BaseModel
from sqlalchemy import Boolean, Enum as SAEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class NoteContentType(str, Enum):
    MARKDOWN = "markdown"
    TABLE = "table"


class Note(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "notes"

    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    content_type: Mapped[NoteContentType] = mapped_column(
        SAEnum(NoteContentType, name="note_content_type"), nullable=False
    )
    archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    text_content: Mapped["TextContent"] = relationship(
        "TextContent", back_populates="note", uselist=False, cascade="all, delete-orphan"
    )
    table_content: Mapped["TableContent"] = relationship(
        "TableContent", back_populates="note", uselist=False, cascade="all, delete-orphan"
    )
    note_tags: Mapped[List["NoteTag"]] = relationship(
        "NoteTag", back_populates="note", cascade="all, delete-orphan"
    )
    note_links_out: Mapped[List["NoteLink"]] = relationship(
        "NoteLink",
        foreign_keys="NoteLink.source_id",
        back_populates="source",
        cascade="all, delete-orphan",
    )
    note_links_in: Mapped[List["NoteLink"]] = relationship(
        "NoteLink",
        foreign_keys="NoteLink.target_id",
        back_populates="target",
        cascade="all, delete-orphan",
    )


class NoteSchema(BaseModel):
    id: UUIDType
    title: str
    content_type: NoteContentType
    archived: bool
    created_at: datetime
    updated_at: datetime
    text_content: Optional["TextContentSchema"] = None
    table_content: Optional["TableContentSchema"] = None

    class Config:
        orm_mode = True


__all__ = ["Note", "NoteSchema", "NoteContentType"]
