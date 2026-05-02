-- MindMesh Database Schema
-- Requires pgvector extension

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    thought_type VARCHAR(50) NOT NULL,
    emotion VARCHAR(50),
    metadata JSONB DEFAULT '{}',
    embedding vector(1536),  -- OpenAI ada-002 dimensions
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Vector similarity index
CREATE INDEX IF NOT EXISTS memories_embedding_idx 
ON memories USING ivfflat (embedding vector_cosine_ops);

-- Filtering indexes
CREATE INDEX IF NOT EXISTS memories_thought_type_idx 
ON memories (thought_type);

CREATE INDEX IF NOT EXISTS memories_emotion_idx 
ON memories (emotion);

CREATE INDEX IF NOT EXISTS memories_created_at_idx 
ON memories (created_at);
