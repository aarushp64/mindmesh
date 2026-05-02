# 🚀 MindMesh Quick Start Guide

## Prerequisites

- Python 3.8+ 
- Node.js 18+
- PostgreSQL with pgvector extension
- OpenAI API key

## Setup Instructions

### 1. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt

# Copy environment file
copy .env.example .env
# Edit .env with your OpenAI API key and database URL
```

### 2. Frontend Setup

```bash
cd frontend
npm install
# Create .env.local with your API endpoint
echo "API_BASE_URL=http://localhost:8000" > .env.local
```

### 3. Database Setup

```sql
-- Create database
CREATE DATABASE mindmesh;
-- Install pgvector extension
CREATE EXTENSION vector;
```

### 4. Run the Application

**Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000` to start feeding your digital twin!

## First Steps

1. **Capture Thoughts**: Go to "Feed Your Twin" and write your first reflection
2. **Chat with Twin**: Start a conversation with your evolving digital self
3. **Explore**: Watch as your twin learns your patterns and personality

## Key Features

- 🧠 **AI Twin Chat**: Conversational interface with memory-backed responses
- 📝 **Thought Capture**: Natural language input with automatic emotion/theme detection
- 🕸️ **Memory Graph**: Vector-based storage of all your thoughts and experiences
- 📊 **Personality Insights**: AI that learns your tone, values, and patterns
- 🔄 **Background Intelligence**: Automated summaries and reflections

## Architecture

```
MindMesh/
├── backend/           # FastAPI + OpenAI + PostgreSQL
├── frontend/          # Next.js + React + Tailwind
└── database/          # PostgreSQL with pgvector
```

Your thoughts are processed through semantic analysis, stored as vector embeddings, and used to train your personal AI reflection engine.

---

**Ready to meet your digital self?** 🚀