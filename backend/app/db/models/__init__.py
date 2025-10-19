"""Model package exports for SQLAlchemy and Pydantic objects."""

from __future__ import annotations

from typing import Iterable

from .base import Base, TimestampMixin, UUIDMixin
from .draft import Draft, DraftSchema
from .link import NoteLink, NoteLinkSchema, NoteLinkType
from .note import Note, NoteContentType, NoteSchema
from .note_tag import NoteTag, NoteTagSchema
from .table_content import TableContent, TableContentSchema
from .table_row import TableRow, TableRowSchema
from .tag import Tag, TagSchema
from .text_content import TextContent, TextContentSchema


def _rebuild_schema_models(models: Iterable[type]) -> None:
    """Ensure all Pydantic schemas rebuild forward references."""

    namespace = {
        "DraftSchema": DraftSchema,
        "NoteSchema": NoteSchema,
        "NoteTagSchema": NoteTagSchema,
        "NoteLinkSchema": NoteLinkSchema,
        "TableContentSchema": TableContentSchema,
        "TableRowSchema": TableRowSchema,
        "TagSchema": TagSchema,
        "TextContentSchema": TextContentSchema,
    }

    for schema in models:
        rebuild = getattr(schema, "model_rebuild", None)
        if callable(rebuild):
            rebuild(_recursive=True, localns=namespace)
            continue
        update = getattr(schema, "update_forward_refs", None)
        if callable(update):
            update(**namespace)


_rebuild_schema_models(
    [
        DraftSchema,
        NoteSchema,
        NoteTagSchema,
        NoteLinkSchema,
        TableContentSchema,
        TableRowSchema,
        TagSchema,
        TextContentSchema,
    ]
)

__all__ = [
    "Base",
    "Draft",
    "DraftSchema",
    "Note",
    "NoteSchema",
    "NoteContentType",
    "NoteLink",
    "NoteLinkSchema",
    "NoteLinkType",
    "NoteTag",
    "NoteTagSchema",
    "TableContent",
    "TableContentSchema",
    "TableRow",
    "TableRowSchema",
    "Tag",
    "TagSchema",
    "TextContent",
    "TextContentSchema",
    "TimestampMixin",
    "UUIDMixin",
]
