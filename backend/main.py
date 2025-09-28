from typing import List, Optional
import os
import re
import json
import logging
import sys

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import numpy as np
from sentence_transformers import SentenceTransformer, util

import crud
from database import Base, engine, get_db
from models import NoteRead, NoteCreate, NoteUpdate, Note

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize the SentenceTransformer model
LOCAL_MODEL_PATH = os.environ.get("MINDMESH_LOCAL_MODEL_PATH")
_model: Optional[SentenceTransformer] = None

def get_model() -> SentenceTransformer:
    global _model
    try:
        if _model is None:
            logger.info("Initializing SentenceTransformer model...")
            model_path = LOCAL_MODEL_PATH or "sentence-transformers/all-MiniLM-L6-v2"
            logger.info(f"Using model path: {model_path}")
            _model = SentenceTransformer(model_path)
            logger.info("Model initialized successfully")
        return _model
    except Exception as e:
        logger.error(f"Error initializing model: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to initialize search model")

app = FastAPI(title="MindMesh Prototype API")

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"},
    )


def classify_layer(title: str, content: str | None) -> str:
    text = f"{title} \n {content or ''}".lower()
    emotional = ["feel", "love", "fear", "anxious", "happy", "sad", "mood", "emotion"]
    creative = ["idea", "brainstorm", "draft", "story", "design", "concept", "poem", "sketch"]
    factual = ["meeting", "notes", "summary", "todo", "task", "research", "cite", "reference"]
    if any(k in text for k in emotional):
        return "emotional"
    if any(k in text for k in creative):
        return "creative"
    if any(k in text for k in factual):
        return "factual"
    return "factual"

# Allow local dev on Vite default port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/notes/search", response_model=List[NoteRead], tags=["search"])
async def search_notes(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    try:
        logger.info(f"Processing search request for query: {q}")
        model = get_model()
        
        # Encode query
        query_vec = model.encode(q, normalize_embeddings=True)
        logger.info(f"Query encoded successfully, shape: {query_vec.shape}")
        
        # Get notes
        notes = crud.list_notes(db)
        logger.info(f"Retrieved {len(notes)} notes from database")
        
        # Calculate similarities
        scored: list[tuple[float, Note]] = []
        for n in notes:
            if not n.embedding:
                logger.debug(f"Note {n.id} has no embedding, skipping")
                continue
                
            try:
                vec = np.array(json.loads(n.embedding), dtype=np.float32)
                if vec.shape != query_vec.shape:
                    logger.warning(f"Note {n.id} has mismatched embedding shape: {vec.shape}")
                    continue
                    
                score = float(np.dot(query_vec, vec) / (np.linalg.norm(query_vec) * (np.linalg.norm(vec) or 1.0)))
                scored.append((score, n))
                logger.debug(f"Note {n.id} scored: {score}")
                
            except Exception as e:
                logger.error(f"Error processing note {n.id}: {str(e)}")
                continue
        
        # Sort and return top results
        scored.sort(key=lambda x: x[0], reverse=True)
        top = [n for _, n in scored[:3]]
        logger.info(f"Returning {len(top)} search results")
        
        return [_to_read(n) for n in top]
        
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Search operation failed")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/notes", response_model=NoteRead)
def create_note(note_in: NoteCreate, db: Session = Depends(get_db)):
    text = f"{note_in.title}\n\n{note_in.content or ''}"
    model = get_model()
    vec = model.encode(text, normalize_embeddings=True).tolist()
    note = crud.create_note(db, note_in, embedding=vec)
    note.layer = classify_layer(note.title, note.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return _to_read(note)


@app.get("/notes/search", response_model=List[NoteRead])
def search_notes(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    model = get_model()
    query_vec = model.encode(q, normalize_embeddings=True)
    notes = crud.list_notes(db)
    scored: list[tuple[float, Note]] = []
    for n in notes:
        if not n.embedding:
            continue
        try:
            vec = np.array(json.loads(n.embedding), dtype=np.float32)
        except Exception:
            continue
        score = float(np.dot(query_vec, vec) / (np.linalg.norm(query_vec) * (np.linalg.norm(vec) or 1.0)))
        scored.append((score, n))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [n for _, n in scored[:3]]
    return [_to_read(n) for n in top]

@app.get("/notes", response_model=List[NoteRead])
def list_notes(db: Session = Depends(get_db)):
    notes = crud.list_notes(db)
    return [_to_read(n) for n in notes]


@app.get("/notes/search", response_model=List[NoteRead])
def search_notes(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    model = get_model()
    query_vec = model.encode(q, normalize_embeddings=True)
    notes = crud.list_notes(db)
    scored: list[tuple[float, Note]] = []
    for n in notes:
        if not n.embedding:
            continue
        try:
            vec = np.array(json.loads(n.embedding), dtype=np.float32)
        except Exception:
            continue
        score = float(np.dot(query_vec, vec) / (np.linalg.norm(query_vec) * (np.linalg.norm(vec) or 1.0)))
        scored.append((score, n))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [n for _, n in scored[:3]]
    return [_to_read(n) for n in top]


@app.get("/notes/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return _to_read(note)


@app.put("/notes/{note_id}", response_model=NoteRead)
def update_note(note_id: int, note_in: NoteUpdate, db: Session = Depends(get_db)):
    embedding = None
    if (note_in.title is not None) or (note_in.content is not None):
        existing = crud.get_note(db, note_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Note not found")
        new_title = note_in.title if note_in.title is not None else existing.title
        new_content = note_in.content if note_in.content is not None else existing.content
        text = f"{new_title}\n\n{new_content or ''}"
        model = get_model()
        embedding = model.encode(text, normalize_embeddings=True).tolist()
    note = crud.update_note(db, note_id, note_in, embedding=embedding)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.layer = classify_layer(note.title, note.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return _to_read(note)


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_note(db, note_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"ok": True}


def extractive_summary(query: str, documents: list[str], model: SentenceTransformer, max_sentences: int = 3) -> str:
    sentences: list[str] = []
    for doc in documents:
        if doc:
            sentences.extend(re.split(r"(?<=[.!?])\s+", doc))
    if not sentences:
        return ""
    q_emb = model.encode(query, convert_to_tensor=True, normalize_embeddings=True)
    s_emb = model.encode(sentences, convert_to_tensor=True, normalize_embeddings=True)
    sims = util.pytorch_cos_sim(q_emb, s_emb)[0]
    idx = np.argsort(sims.cpu().numpy())[-max_sentences:]
    picked = [sentences[i] for i in sorted(idx)]
    return " ".join(picked)


@app.get("/chat")
def chat(q: str = Query(..., min_length=3), db: Session = Depends(get_db)):
    model = get_model()
    query_vec = model.encode(q, normalize_embeddings=True)
    notes = crud.list_notes(db)
    scored: list[tuple[float, Note]] = []
    for n in notes:
        if not n.embedding:
            continue
        try:
            vec = np.array(json.loads(n.embedding), dtype=np.float32)
        except Exception:
            continue
        score = float(np.dot(query_vec, vec) / (np.linalg.norm(query_vec) * (np.linalg.norm(vec) or 1.0)))
        scored.append((score, n))
    scored.sort(key=lambda x: x[0], reverse=True)
    top_notes = [n for _, n in scored[:5]]
    if not top_notes:
        return {"answer": "I couldn't find relevant notes yet. Try adding more notes.", "notes": []}
    docs = [n.content for n in top_notes if n.content]
    summary = extractive_summary(q, docs, model, max_sentences=3)
    if not summary:
        context = "\n\n".join([f"- {n.title}: {n.content or ''}" for n in top_notes[:3]])
        summary = f"Based on your notes, here are relevant points for '{q}':\n" + context
    return {"answer": summary, "notes": [_to_read(n) for n in top_notes[:3]]}


@app.get("/nudges", response_model=List[NoteRead])
def get_nudges(db: Session = Depends(get_db), layer: Optional[str] = Query(None, enum=["factual", "creative", "emotional"]), frequency: str = Query("daily", enum=["daily", "weekly", "all"])):
    notes = crud.list_notes(db)
    if layer:
        notes = [n for n in notes if n.layer == layer]
    if frequency != "all":
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        threshold = now - (timedelta(days=1) if frequency == "daily" else timedelta(days=7))
        notes = [n for n in notes if (n.updated_at or n.created_at) < threshold]
    notes.sort(key=lambda n: n.updated_at or n.created_at)
    return [_to_read(n) for n in notes[:3]]


def _to_read(note: Note) -> NoteRead:
    return NoteRead(
        id=note.id,
        title=note.title,
        content=note.content,
        layer=note.layer,
        created_at=note.created_at,
        updated_at=note.updated_at,
        links=[ln.id for ln in note.links] if note.links else [],
        tags=note.tags,
    )




