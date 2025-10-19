"""SQLAlchemy model and Pydantic schema for Draft."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType

from pydantic import BaseModel
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, UUIDMixin


class Draft(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "drafts"

    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    editor_state: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    metadata: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class DraftSchema(BaseModel):
    id: UUIDType
    title: Optional[str]
    body: Optional[str]
    editor_state: dict
    metadata: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


__all__ = ["Draft", "DraftSchema"]
