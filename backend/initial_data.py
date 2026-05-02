"""
Initial data loader for pre-loaded notes about the project.
"""
import json
from typing import List, Dict
from sentence_transformers import SentenceTransformer

from models import NoteCreate
import crud
from database import SessionLocal

INITIAL_NOTES = [
    {
        "title": "MindMesh: AI-Powered Note Taking",
        "content": """MindMesh is an innovative note-taking application that combines human creativity with artificial intelligence. 
        It features automatic tagging, semantic search, and intelligent note linking to help users organize their thoughts effortlessly.
        The project uses React for the frontend, FastAPI for the backend, and integrates advanced AI features through sentence transformers.""",
        "tags": ["project", "overview", "ai", "tech"],
        "layer": "factual"
    },
    {
        "title": "Smart Features in MindMesh",
        "content": """MindMesh's key features include:
        1. Automatic title extraction from content
        2. AI-powered tag generation
        3. Semantic similarity search
        4. Automatic note linking
        5. Content classification
        6. Dark/light mode theming
        
        The AI features use sentence transformers to understand the context and meaning of notes, making organization effortless.""",
        "tags": ["features", "ai", "documentation"],
        "layer": "factual"
    },
    {
        "title": "Using Quick Note Mode",
        "content": """Quick Note Mode allows you to write your thoughts naturally without worrying about organization. 
        Just write your ideas, and the AI will:
        - Generate an appropriate title
        - Add relevant tags
        - Find related notes
        - Classify the content
        - Create semantic embeddings
        
        This makes note-taking more intuitive while maintaining organization.""",
        "tags": ["tutorial", "quicknote", "usage"],
        "layer": "creative"
    },
    {
        "title": "Technical Architecture",
        "content": """MindMesh's architecture combines modern web technologies with AI:
        
        Frontend:
        - React for UI components
        - Tailwind CSS for styling
        - Dark/light mode theming
        
        Backend:
        - FastAPI for the REST API
        - SQLAlchemy for database management
        - Sentence Transformers for AI features
        
        The application uses semantic embeddings to understand note relationships.""",
        "tags": ["architecture", "technical", "documentation"],
        "layer": "factual"
    },
    {
        "title": "Future Development Ideas",
        "content": """Potential future enhancements for MindMesh:
        1. Collaborative note-taking features
        2. Real-time note synchronization
        3. Enhanced visualization options
        4. Mobile application
        5. Integration with other note-taking tools
        6. Enhanced AI features for better context understanding
        
        These improvements would make MindMesh an even more powerful tool for knowledge management.""",
        "tags": ["roadmap", "ideas", "future"],
        "layer": "creative"
    }
]

def create_initial_embeddings(notes: List[Dict], model: SentenceTransformer) -> List[Dict]:
    """Create embeddings for initial notes."""
    for note in notes:
        text = f"{note['title']}\n{note['content']}"
        note['embedding'] = model.encode(text, normalize_embeddings=True).tolist()
    return notes

def create_initial_notes(model: SentenceTransformer):
    """Create initial notes in the database."""
    db = SessionLocal()
    try:
        # Check if we already have notes
        existing = crud.list_notes(db)
        if existing:
            print("Database already contains notes, skipping initialization")
            return

        # Create embeddings for all notes
        notes_with_embeddings = create_initial_embeddings(INITIAL_NOTES, model)
        
        # Create notes and store their IDs
        note_ids = {}
        for note_data in notes_with_embeddings:
            note = crud.create_note(
                db,
                NoteCreate(
                    title=note_data['title'],
                    content=note_data['content'],
                    tags=note_data['tags'],
                    layer=note_data['layer'],
                    link_ids=[]
                ),
                embedding=note_data['embedding']
            )
            note_ids[note_data['title']] = note.id

        # Create links between related notes
        links = [
            ("MindMesh: AI-Powered Note Taking", ["Smart Features in MindMesh", "Technical Architecture"]),
            ("Smart Features in MindMesh", ["Using Quick Note Mode", "Technical Architecture"]),
            ("Using Quick Note Mode", ["Smart Features in MindMesh"]),
            ("Technical Architecture", ["Future Development Ideas"]),
            ("Future Development Ideas", ["Smart Features in MindMesh"])
        ]

        # Update notes with links
        for source, targets in links:
            source_id = note_ids[source]
            target_ids = [note_ids[target] for target in targets]
            crud.update_note(
                db,
                source_id,
                NoteCreate(
                    title=source,
                    link_ids=target_ids
                )
            )

        print("Successfully created initial notes")
        
    except Exception as e:
        print(f"Error creating initial notes: {str(e)}")
        raise
    finally:
        db.close()