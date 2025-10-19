"""Association table model and schema for Note and Tag relationship."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID as UUIDType

from pydantic import BaseModel
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class NoteTag(TimestampMixin, Base):
    __tablename__ = "note_tags"
    __table_args__ = (
        PrimaryKeyConstraint("note_id", "tag_id", name="pk_note_tag"),
    )

    note_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"), nullable=False
    )
    tag_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"), nullable=False
    )

    note: Mapped["Note"] = relationship("Note", back_populates="note_tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="note_tags")


class NoteTagSchema(BaseModel):
    note_id: UUIDType
    tag_id: UUIDType
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


__all__ = ["NoteTag", "NoteTagSchema"]
