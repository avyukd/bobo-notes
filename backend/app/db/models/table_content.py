"""SQLAlchemy model and Pydantic schema for TableContent."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID as UUIDType

from pydantic import BaseModel
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class TableContent(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "table_contents"

    note_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    schema_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    row_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    note: Mapped["Note"] = relationship("Note", back_populates="table_content")
    rows: Mapped[list["TableRow"]] = relationship(
        "TableRow",
        back_populates="table_content",
        cascade="all, delete-orphan",
        primaryjoin="TableContent.note_id==TableRow.table_note_id",
        foreign_keys="TableRow.table_note_id",
    )


class TableContentSchema(BaseModel):
    id: UUIDType
    note_id: UUIDType
    schema_json: dict
    row_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


__all__ = ["TableContent", "TableContentSchema"]
