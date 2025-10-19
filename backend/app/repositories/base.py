"""Shared base repository functionality."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """Base repository that wraps an :class:`AsyncSession`."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit_and_refresh(self, entity: Any) -> Any:
        """Commit the current transaction and refresh the given entity."""

        await self.session.commit()
        await self.session.refresh(entity)
        return entity
