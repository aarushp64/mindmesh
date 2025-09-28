from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, field_validator
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


# Association table for many-to-many note links (edges)
note_links = Table(
    "note_links",
    Base.metadata,
    Column("from_note_id", ForeignKey("notes.id"), primary_key=True),
    Column("to_note_id", ForeignKey("notes.id"), primary_key=True),
)


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    # Layer classification: factual, creative, emotional
    layer: Mapped[str | None] = mapped_column(String(32), nullable=True)
    # Comma-separated tags string for simple storage
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)
    # JSON-serialized embedding vector (list of floats)
    embedding: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Graph-style links
    links: Mapped[list["Note"]] = relationship(
        "Note",
        secondary=note_links,
        primaryjoin=lambda: Note.id == note_links.c.from_note_id,
        secondaryjoin=lambda: Note.id == note_links.c.to_note_id,
        backref="backlinks",
    )


# Pydantic schemas
class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = None
    link_ids: list[int] = []
    tags: list[str] = []


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    link_ids: Optional[list[int]] = None
    tags: Optional[list[str]] = None


class NoteRead(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    layer: Optional[str] = None
    tags: list[str] = []
    created_at: datetime
    updated_at: datetime
    links: list[int] = []

    @field_validator("tags", mode="before")
    @classmethod
    def split_tags(cls, v: Any) -> list[str]:
        if isinstance(v, str) and v:
            return [t.strip() for t in v.split(',') if t.strip()]
        elif isinstance(v, list):
            return v
        return []

    class Config:
        from_attributes = True




