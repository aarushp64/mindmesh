# 🧠💫 MindMesh: Your AI Digital Twin

> "Not just your notes — your mind, evolving beside you."

MindMesh is an AI reflection engine that grows from your thoughts, mirrors your personality, and helps you think, plan, and act like a second consciousness.

## 🌟 Core Concept

Every thought you feed it becomes part of its soul. MindMesh becomes your digital twin - understanding your patterns, remembering what you forget, and reflecting your inner world back to you with wisdom and clarity.

## 🧩 Architecture

```
mindmesh/
├── frontend/          # React/Next.js chat interface
├── backend/           # FastAPI server with AI processing
├── database/          # PostgreSQL with pgvector for memories
└── ai-engine/         # LLM integration and personality modeling
```

## 🚀 Features

- **Thought Capture**: Natural language input for ideas, plans, memories, goals
- **AI Twin Chat**: Conversational interface with your evolving digital self
- **Memory Graph**: Vector-based storage of all your thoughts and experiences
- **Personality Reflection**: AI that learns your tone, values, and patterns
- **Background Intelligence**: Automated insights, summaries, and reflections
- **Mind Visualization**: Interactive graph of your thought network

## 🛠️ Tech Stack

- **Frontend**: Next.js, React, Tailwind CSS, Framer Motion
- **Backend**: FastAPI, Python, Celery (async tasks)
- **Database**: PostgreSQL with pgvector extension
- **AI/ML**: OpenAI GPT-4, LangChain, custom embeddings
- **Deployment**: Vercel (frontend), Render (backend), Neon (database)

## 📦 Installation

```bash
# Clone and setup
git clone <repository-url> mindmesh
cd mindmesh

# Setup backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install

# Setup environment variables
cp .env.example .env
# Add your OpenAI API key and database URL
```

## 🚀 Running the Project

```bash
# Start backend (from backend/)
uvicorn main:app --reload

# Start frontend (from frontend/)
npm run dev
```

## 🧠 How It Works

1. **Input**: You share thoughts, ideas, plans, or reflections
2. **Processing**: AI analyzes semantics, emotion, and context
3. **Memory**: Thoughts are embedded and stored in vector database
4. **Reflection**: Your AI twin responds with contextual understanding
5. **Growth**: The twin evolves its personality model over time

## 📝 Example Interactions

```
You: "I feel like I'm losing focus lately on my creative projects."

Twin: "I remember you mentioned feeling scattered about your creative work 
three weeks ago too. Back then, you said morning sessions helped you focus. 
You also wrote about wanting to 'create something that truly represents me' 
- maybe that's calling to you again?"
```

Your twin remembers, understands, and reflects your journey back to you.

---

*Building your digital reflection, one thought at a time.*