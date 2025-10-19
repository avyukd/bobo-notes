"""SQLAlchemy model and Pydantic schema for Tag."""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID as UUIDType

from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Tag(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)

    note_tags: Mapped[List["NoteTag"]] = relationship(
        "NoteTag", back_populates="tag", cascade="all, delete-orphan"
    )


class TagSchema(BaseModel):
    id: UUIDType
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


__all__ = ["Tag", "TagSchema"]
