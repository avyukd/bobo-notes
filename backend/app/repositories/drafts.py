"""Repository for working with :class:`~app.db.models.Draft` objects."""

from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select

from ..db.models import Draft
from .base import BaseRepository


class DraftRepository(BaseRepository):
    """CRUD helpers for :class:`Draft`."""

    async def list(self) -> List[Draft]:
        stmt = select(Draft).order_by(Draft.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().unique())

    async def get(self, draft_id: UUID) -> Optional[Draft]:
        stmt = select(Draft).where(Draft.id == draft_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, title: Optional[str] = None, body: Optional[str] = None) -> Draft:
        draft = Draft(title=title, body=body)
        self.session.add(draft)
        return await self.commit_and_refresh(draft)

    async def delete(self, draft_id: UUID) -> bool:
        draft = await self.get(draft_id)
        if draft is None:
            return False

        await self.session.delete(draft)
        await self.session.commit()
        return True
