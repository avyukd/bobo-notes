"""Repository helpers for :class:`~app.db.models.Tag`."""

from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..db.models import Tag
from .base import BaseRepository


class TagRepository(BaseRepository):
    """Simple CRUD helpers for :class:`Tag`."""

    async def get_or_create(self, name: str) -> Tag:
        stmt = select(Tag).where(Tag.name == name)
        result = await self.session.execute(stmt)
        tag = result.scalar_one_or_none()
        if tag is not None:
            return tag

        tag = Tag(name=name)
        self.session.add(tag)
        try:
            return await self.commit_and_refresh(tag)
        except IntegrityError:
            await self.session.rollback()
            result = await self.session.execute(stmt)
            existing = result.scalar_one()
            return existing

    async def list_all(self) -> List[Tag]:
        stmt = select(Tag).order_by(Tag.name.asc())
        result = await self.session.execute(stmt)
        return list(result.scalars().unique())
