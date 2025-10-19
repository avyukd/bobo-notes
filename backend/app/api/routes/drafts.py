"""HTTP routes for working with drafts."""

from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.models import DraftSchema
from ...db.session import get_db
from ...repositories import DraftRepository
from ..schemas import to_schema
from .schemas import DraftCreate

router = APIRouter()


@router.get("/", response_model=List[DraftSchema])
async def list_drafts(session: AsyncSession = Depends(get_db)) -> List[DraftSchema]:
    repo = DraftRepository(session)
    drafts = await repo.list()
    return [to_schema(DraftSchema, draft) for draft in drafts]


@router.get("/{draft_id}", response_model=DraftSchema)
async def get_draft(
    draft_id: UUID, session: AsyncSession = Depends(get_db)
) -> DraftSchema:
    repo = DraftRepository(session)
    draft = await repo.get(draft_id)
    if draft is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Draft not found")
    return to_schema(DraftSchema, draft)


@router.post("/", response_model=DraftSchema, status_code=status.HTTP_201_CREATED)
async def create_draft(
    payload: DraftCreate, session: AsyncSession = Depends(get_db)
) -> DraftSchema:
    repo = DraftRepository(session)
    draft = await repo.create(title=payload.title, body=payload.body)
    return to_schema(DraftSchema, draft)


@router.delete("/{draft_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_draft(
    draft_id: UUID, session: AsyncSession = Depends(get_db)
) -> Response:
    repo = DraftRepository(session)
    deleted = await repo.delete(draft_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Draft not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
