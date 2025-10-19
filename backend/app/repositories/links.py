"""Repository helpers for creating links between notes."""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from ..db.models import NoteLink, NoteLinkType
from .base import BaseRepository


class LinkRepository(BaseRepository):
    """Persistence helpers for :class:`NoteLink`."""

    async def create_link(
        self,
        source_id: UUID,
        target_id: UUID,
        link_type: str | NoteLinkType,
        context_excerpt: Optional[str] = None,
    ) -> NoteLink:
        if not isinstance(link_type, NoteLinkType):
            link_type = NoteLinkType(link_type)

        link = NoteLink(
            source_id=source_id,
            target_id=target_id,
            link_type=link_type,
            context_excerpt=context_excerpt,
        )
        self.session.add(link)
        return await self.commit_and_refresh(link)
