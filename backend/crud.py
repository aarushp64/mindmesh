from typing import Iterable, List, Optional
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Note, NoteCreate, NoteUpdate


def create_note(db: Session, note_in: NoteCreate, embedding: Optional[List[float]] = None) -> Note:
    note = Note(
        title=note_in.title,
        content=note_in.content,
        embedding=json.dumps(embedding) if embedding is not None else None,
        tags=",".join(note_in.tags) if getattr(note_in, "tags", None) else None,
    )
    if note_in.link_ids:
        linked_notes = db.scalars(select(Note).where(Note.id.in_(note_in.link_ids))).all()
        note.links = list(linked_notes)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_note(db: Session, note_id: int) -> Optional[Note]:
    return db.get(Note, note_id)


def list_notes(db: Session) -> List[Note]:
    return list(db.scalars(select(Note)).all())


def update_note(db: Session, note_id: int, note_in: NoteUpdate, embedding: Optional[List[float]] = None) -> Optional[Note]:
    note = db.get(Note, note_id)
    if not note:
        return None
    if note_in.title is not None:
        note.title = note_in.title
    if note_in.content is not None:
        note.content = note_in.content
    if embedding is not None:
        note.embedding = json.dumps(embedding)
    if note_in.link_ids is not None:
        linked_notes = db.scalars(select(Note).where(Note.id.in_(note_in.link_ids))).all()
        note.links = list(linked_notes)
    if getattr(note_in, "tags", None) is not None:
        note.tags = ",".join(note_in.tags) if note_in.tags else None
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note_id: int) -> bool:
    note = db.get(Note, note_id)
    if not note:
        return False
    db.delete(note)
    db.commit()
    return True




