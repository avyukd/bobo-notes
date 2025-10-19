"""Database session and engine configuration."""

from __future__ import annotations

import os
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/bobo_notes",
)


def get_engine() -> AsyncEngine:
    """Create a new SQLAlchemy async engine instance."""

    return create_async_engine(DATABASE_URL, echo=False, future=True)


def get_session(engine: Optional[AsyncEngine] = None) -> async_sessionmaker[AsyncSession]:
    """Create an async session factory bound to the provided engine."""

    return async_sessionmaker(
        bind=engine or get_engine(),
        expire_on_commit=False,
        class_=AsyncSession,
    )


engine = get_engine()
SessionLocal = get_session(engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async database session."""

    async with SessionLocal() as session:
        yield session


__all__ = ["SessionLocal", "engine", "get_db", "get_engine", "get_session"]
