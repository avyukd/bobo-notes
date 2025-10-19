"""Helper utilities for working with Pydantic schemas."""

from __future__ import annotations

from typing import Any, Callable, Type, TypeVar

T = TypeVar("T")


def to_schema(schema_cls: Type[T], entity: Any) -> T:
    """Return a Pydantic schema instance for the given ORM entity."""

    validator: Callable[..., T] | None = getattr(schema_cls, "model_validate", None)
    if callable(validator):
        return validator(entity, from_attributes=True)

    fallback = getattr(schema_cls, "from_orm", None)
    if callable(fallback):
        return fallback(entity)

    raise TypeError(f"Schema {schema_cls!r} does not support ORM conversion")
