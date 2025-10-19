"""Service function that simulates organizing a draft into a note."""

from __future__ import annotations

from typing import Callable
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ...db.models import NoteContentType, NoteSchema
from ...repositories import DraftRepository, NoteRepository


def _note_to_schema(note) -> NoteSchema:
    validator: Callable[..., NoteSchema] | None = getattr(NoteSchema, "model_validate", None)
    if callable(validator):
        return validator(note, from_attributes=True)

    fallback = getattr(NoteSchema, "from_orm", None)
    if callable(fallback):
        return fallback(note)

    raise TypeError("NoteSchema cannot be constructed from ORM object")


async def organize_draft(session: AsyncSession, draft_id: UUID) -> NoteSchema:
    """Convert a draft into a persisted note and delete the draft."""

    draft_repo = DraftRepository(session)
    draft = await draft_repo.get(draft_id)
    if draft is None:
        raise ValueError("Draft not found")

    title = draft.title or "Untitled Draft"
    body = draft.body or ""

    note_repo = NoteRepository(session)
    note = await note_repo.create(
        title=title,
        content_type=NoteContentType.MARKDOWN,
        body=body,
    )

    await draft_repo.delete(draft_id)
    return _note_to_schema(note)
