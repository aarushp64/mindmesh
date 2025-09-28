# MindMesh Prototype

A note-taking application with semantic search capabilities and graph-like connections between notes.

## Features

- Create, read, update, and delete notes
- Add tags to notes
- Link notes together to create a knowledge graph
- Semantic search using sentence transformers
- Simple graph visualization
- Markdown support for note content
- Auto-classification of notes into factual, creative, and emotional layers

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm
- Windows (tested on Windows 10/11)

## Project Structure

```
mindmesh-prototype/
├── backend/                # FastAPI backend
│   ├── __init__.py
│   ├── main.py            # API endpoints and server config
│   ├── models.py          # Database models and Pydantic schemas
│   ├── database.py        # Database configuration
│   ├── crud.py            # CRUD operations
│   └── requirements.txt   # Python dependencies
├── frontend/              # React frontend
│   ├── src/
│   │   ├── App.jsx       # Main application component
│   │   └── components/   # React components
│   ├── package.json      # Node.js dependencies
│   └── vite.config.js    # Vite configuration
└── app.db                # SQLite database file (created on first run)
```

## Installation

### Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r backend\requirements.txt
```

3. (Optional) Set local model path to avoid download:
```bash
set MINDMESH_LOCAL_MODEL_PATH=C:\path\to\all-MiniLM-L6-v2
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

## Running the Application

### Start the Backend

1. From the project root:
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

2. Verify the server is running:
   - Open http://127.0.0.1:8000/health in your browser
   - You should see `{"status":"ok"}`

### Start the Frontend

1. In a new terminal, from the frontend directory:
```bash
npm run dev
```

2. Open http://127.0.0.1:5173 in your browser

## Usage

1. Create a note:
   - Fill in the note content
   - Add optional tags (comma-separated)
   - Link to other notes by ID if desired

2. View notes:
   - Notes are displayed in the list view with Markdown rendering
   - Connected notes are shown in the graph view

3. Search:
   - Use the search box to find semantically similar notes
   - Results are ranked by relevance

4. Delete notes:
   - Click the "Delete" button on any note

## Troubleshooting

### Model Download Issues
- First run will download the sentence-transformer model
- Ensure internet connectivity
- Or set MINDMESH_LOCAL_MODEL_PATH environment variable

### CORS Errors
- Ensure backend runs on http://127.0.0.1:8000
- Ensure frontend runs on http://127.0.0.1:5173

### Database Location
- SQLite database (app.db) is created relative to working directory
- Run uvicorn from project root for consistent path resolution

### Python Dependencies
- Ensure Python 3.10+ is installed
- Update pip if needed: `python -m pip install --upgrade pip`
- On Windows, you may need Visual C++ Build Tools for some packages

## License

MIT License