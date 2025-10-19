"""Routes that simulate AI organization of drafts into notes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.models import NoteSchema
from ...db.session import get_db
from ...services.ai import organize_draft as organize_draft_service

router = APIRouter()


@router.post("/{draft_id}", response_model=NoteSchema)
async def organize_draft(
    draft_id: UUID, session: AsyncSession = Depends(get_db)
) -> NoteSchema:
    try:
        return await organize_draft_service(session, draft_id)
    except ValueError as exc:  # draft not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
