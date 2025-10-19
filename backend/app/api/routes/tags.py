"""HTTP routes for working with tags."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.models import TagSchema
from ...db.session import get_db
from ...repositories import TagRepository
from ..schemas import to_schema
from .schemas import TagCreate

router = APIRouter()


@router.get("/", response_model=List[TagSchema])
async def list_tags(session: AsyncSession = Depends(get_db)) -> List[TagSchema]:
    repo = TagRepository(session)
    tags = await repo.list_all()
    return [to_schema(TagSchema, tag) for tag in tags]


@router.post("/", response_model=TagSchema)
async def create_tag(
    payload: TagCreate, session: AsyncSession = Depends(get_db)
) -> TagSchema:
    repo = TagRepository(session)
    tag = await repo.get_or_create(payload.name)
    return to_schema(TagSchema, tag)
