"""SQLAlchemy model and Pydantic schema for TableRow."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType

from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class TableRow(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "table_rows"

    table_note_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("table_contents.note_id", ondelete="CASCADE"), nullable=False
    )
    row_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    embedding: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    table_content: Mapped["TableContent"] = relationship(
        "TableContent",
        back_populates="rows",
        primaryjoin="TableRow.table_note_id==TableContent.note_id",
        foreign_keys=[table_note_id],
    )


class TableRowSchema(BaseModel):
    id: UUIDType
    table_note_id: UUIDType
    row_data: dict
    embedding: Optional[dict]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


__all__ = ["TableRow", "TableRowSchema"]
