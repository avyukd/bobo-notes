"""Repository for working with :class:`~app.db.models.Note` objects."""

from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..db.models import Note, NoteContentType, TextContent
from .base import BaseRepository


class NoteRepository(BaseRepository):
    """CRUD helpers for :class:`Note`."""

    async def list(self, limit: int = 50) -> List[Note]:
        """Return the newest notes up to ``limit`` records."""

        stmt = (
            select(Note)
            .options(selectinload(Note.text_content))
            .order_by(Note.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().unique())

    async def get(self, note_id: UUID) -> Optional[Note]:
        """Return a single note by its identifier."""

        stmt = (
            select(Note)
            .options(selectinload(Note.text_content))
            .where(Note.id == note_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self, title: str, content_type: str | NoteContentType, body: Optional[str] = None
    ) -> Note:
        """Create a new note and optional text content."""

        if not isinstance(content_type, NoteContentType):
            content_type = NoteContentType(content_type)

        note = Note(title=title, content_type=content_type)
        self.session.add(note)
        await self.session.flush()

        if content_type == NoteContentType.MARKDOWN:
            text_content = TextContent(note_id=note.id, body=body or "")
            self.session.add(text_content)

        return await self.commit_and_refresh(note)

    async def update(self, note_id: UUID, **fields: object) -> Optional[Note]:
        """Update the provided fields on a note."""

        note = await self.get(note_id)
        if note is None:
            return None

        content_type = fields.pop("content_type", None)
        if content_type is not None:
            if not isinstance(content_type, NoteContentType):
                content_type = NoteContentType(content_type)
            note.content_type = content_type

        title = fields.pop("title", None)
        if title is not None:
            note.title = str(title)

        archived = fields.pop("archived", None)
        if archived is not None:
            note.archived = bool(archived)

        if "body" in fields:
            body = fields.pop("body")
            if body is not None:
                text = note.text_content
                if text is None:
                    text = TextContent(note_id=note.id, body=str(body))
                    self.session.add(text)
                else:
                    text.body = str(body)
            elif note.text_content is not None:
                note.text_content.body = ""

        return await self.commit_and_refresh(note)

    async def delete(self, note_id: UUID) -> bool:
        """Delete a note by id. Returns ``True`` if it existed."""

        note = await self.get(note_id)
        if note is None:
            return False

        await self.session.delete(note)
        await self.session.commit()
        return True
