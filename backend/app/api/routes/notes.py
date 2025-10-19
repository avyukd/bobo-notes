"""HTTP routes for working with notes."""

from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.models import NoteSchema
from ...db.session import get_db
from ...repositories import NoteRepository
from ..schemas import to_schema
from .schemas import NoteCreate, NoteUpdate

router = APIRouter()


@router.get("/", response_model=List[NoteSchema])
async def list_notes(
    limit: int = Query(default=50, ge=1, le=200),
    session: AsyncSession = Depends(get_db),
) -> List[NoteSchema]:
    repo = NoteRepository(session)
    notes = await repo.list(limit=limit)
    return [to_schema(NoteSchema, note) for note in notes]


@router.get("/{note_id}", response_model=NoteSchema)
async def get_note(
    note_id: UUID, session: AsyncSession = Depends(get_db)
) -> NoteSchema:
    repo = NoteRepository(session)
    note = await repo.get(note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return to_schema(NoteSchema, note)


@router.post("/", response_model=NoteSchema, status_code=status.HTTP_201_CREATED)
async def create_note(
    payload: NoteCreate, session: AsyncSession = Depends(get_db)
) -> NoteSchema:
    repo = NoteRepository(session)
    note = await repo.create(
        title=payload.title,
        content_type=payload.content_type,
        body=payload.body,
    )
    return to_schema(NoteSchema, note)


@router.patch("/{note_id}", response_model=NoteSchema)
async def update_note(
    note_id: UUID, payload: NoteUpdate, session: AsyncSession = Depends(get_db)
) -> NoteSchema:
    repo = NoteRepository(session)
    data = payload.dict(exclude_unset=True)
    note = await repo.update(note_id, **data)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return to_schema(NoteSchema, note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: UUID, session: AsyncSession = Depends(get_db)
) -> Response:
    repo = NoteRepository(session)
    deleted = await repo.delete(note_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
