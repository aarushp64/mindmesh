import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import asyncpg
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

load_dotenv()

class MemoryEngine:
    """Core memory system using vector embeddings for semantic storage and retrieval"""
    
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.db_pool = None
        self.embedding_model = "text-embedding-ada-002"
        
    async def initialize_db(self):
        """Initialize database connection and create tables if they don't exist"""
        if not self.db_pool:
            database_url = os.getenv("DATABASE_URL", "postgresql://localhost/mindmesh")
            self.db_pool = await asyncpg.create_pool(database_url)
            
            # Create tables for memories and embeddings
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
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
                    
                    CREATE INDEX IF NOT EXISTS memories_embedding_idx 
                    ON memories USING ivfflat (embedding vector_cosine_ops);
                    
                    CREATE INDEX IF NOT EXISTS memories_thought_type_idx 
                    ON memories (thought_type);
                    
                    CREATE INDEX IF NOT EXISTS memories_emotion_idx 
                    ON memories (emotion);
                    
                    CREATE INDEX IF NOT EXISTS memories_created_at_idx 
                    ON memories (created_at);
                """)
    
    async def create_embedding(self, text: str) -> List[float]:
        """Create vector embedding for text using OpenAI"""
        try:
            response = await self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error creating embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * 1536
    
    async def store_memory(
        self, 
        content: str, 
        thought_type: str, 
        emotion: str, 
        metadata: Dict[str, Any] = None
    ) -> str:
        """Store a memory with its vector embedding"""
        await self.initialize_db()
        
        # Create embedding for the content
        embedding = await self.create_embedding(content)
        
        # Store in database
        async with self.db_pool.acquire() as conn:
            memory_id = await conn.fetchval("""
                INSERT INTO memories (content, thought_type, emotion, metadata, embedding)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id
            """, content, thought_type, emotion, json.dumps(metadata or {}), embedding)
            
        return str(memory_id)
    
    async def retrieve_memories(
        self, 
        query: str, 
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Retrieve memories most similar to query using vector similarity"""
        await self.initialize_db()
        
        # Create embedding for query
        query_embedding = await self.create_embedding(query)
        
        # Find similar memories
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT 
                    id, content, thought_type, emotion, metadata, created_at,
                    1 - (embedding <=> $1) as similarity
                FROM memories
                WHERE 1 - (embedding <=> $1) > $2
                ORDER BY embedding <=> $1
                LIMIT $3
            """, query_embedding, similarity_threshold, limit)
            
        return [
            {
                "id": str(row["id"]),
                "content": row["content"],
                "thought_type": row["thought_type"],
                "emotion": row["emotion"],
                "metadata": json.loads(row["metadata"]),
                "created_at": row["created_at"].isoformat(),
                "similarity": float(row["similarity"])
            }
            for row in rows
        ]
    
    async def get_memories(
        self,
        limit: int = 20,
        thought_type: Optional[str] = None,
        emotion: Optional[str] = None,
        since: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get memories with optional filtering"""
        await self.initialize_db()
        
        query = "SELECT id, content, thought_type, emotion, metadata, created_at FROM memories"
        conditions = []
        params = []
        
        if thought_type:
            conditions.append(f"thought_type = ${len(params) + 1}")
            params.append(thought_type)
            
        if emotion:
            conditions.append(f"emotion = ${len(params) + 1}")
            params.append(emotion)
            
        if since:
            conditions.append(f"created_at >= ${len(params) + 1}")
            params.append(since)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += f" ORDER BY created_at DESC LIMIT ${len(params) + 1}"
        params.append(limit)
        
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
        
        return [
            {
                "id": str(row["id"]),
                "content": row["content"],
                "thought_type": row["thought_type"],
                "emotion": row["emotion"],
                "metadata": json.loads(row["metadata"]),
                "created_at": row["created_at"].isoformat()
            }
            for row in rows
        ]
    
    async def get_memory_clusters(self, num_clusters: int = 5) -> List[Dict[str, Any]]:
        """Get thematic clusters of memories for visualization"""
        await self.initialize_db()
        
        async with self.db_pool.acquire() as conn:
            # Get recent memories with embeddings
            rows = await conn.fetch("""
                SELECT id, content, thought_type, emotion, embedding, created_at
                FROM memories
                WHERE created_at >= NOW() - INTERVAL '30 days'
                ORDER BY created_at DESC
                LIMIT 100
            """)
        
        if not rows:
            return []
        
        # Simple clustering based on thought types and emotions for now
        clusters = {}
        for row in rows:
            key = f"{row['thought_type']}_{row['emotion']}"
            if key not in clusters:
                clusters[key] = {
                    "theme": f"{row['thought_type'].title()} - {row['emotion'].title()}",
                    "memories": [],
                    "count": 0
                }
            
            clusters[key]["memories"].append({
                "id": str(row["id"]),
                "content": row["content"][:200] + "..." if len(row["content"]) > 200 else row["content"],
                "created_at": row["created_at"].isoformat()
            })
            clusters[key]["count"] += 1
        
        # Return top clusters
        return sorted(clusters.values(), key=lambda x: x["count"], reverse=True)[:num_clusters]
    
    async def get_mind_graph(self) -> Dict[str, Any]:
        """Generate graph data for mind visualization"""
        await self.initialize_db()
        
        async with self.db_pool.acquire() as conn:
            # Get memories from last 60 days
            rows = await conn.fetch("""
                SELECT id, content, thought_type, emotion, created_at
                FROM memories
                WHERE created_at >= NOW() - INTERVAL '60 days'
                ORDER BY created_at DESC
                LIMIT 200
            """)
        
        nodes = []
        edges = []
        
        # Create nodes for each memory
        for i, row in enumerate(rows):
            nodes.append({
                "id": str(row["id"]),
                "label": row["content"][:50] + "..." if len(row["content"]) > 50 else row["content"],
                "type": row["thought_type"],
                "emotion": row["emotion"],
                "size": min(len(row["content"]) / 10, 50),  # Size based on content length
                "created_at": row["created_at"].isoformat()
            })
        
        # Create edges based on temporal proximity and theme similarity
        for i, row1 in enumerate(rows[:-1]):
            for j, row2 in enumerate(rows[i+1:], i+1):
                # Connect if same type or created within 24 hours
                time_diff = abs((row1["created_at"] - row2["created_at"]).total_seconds())
                
                if (row1["thought_type"] == row2["thought_type"] or 
                    row1["emotion"] == row2["emotion"] or 
                    time_diff < 86400):  # 24 hours
                    
                    # Limit connections to avoid clutter
                    if len(edges) < 300:
                        edges.append({
                            "source": str(row1["id"]),
                            "target": str(row2["id"]),
                            "strength": 1 / (time_diff / 3600 + 1)  # Stronger for closer in time
                        })
        
        return {"nodes": nodes, "edges": edges}
    
    async def delete_memory(self, memory_id: str):
        """Delete a specific memory"""
        await self.initialize_db()
        
        async with self.db_pool.acquire() as conn:
            await conn.execute("DELETE FROM memories WHERE id = $1", uuid.UUID(memory_id))
    
    async def get_emotional_timeline(self, days: int = 30) -> Dict[str, Any]:
        """Get emotional patterns over time"""
        await self.initialize_db()
        
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT 
                    DATE(created_at) as date,
                    emotion,
                    COUNT(*) as count
                FROM memories
                WHERE created_at >= NOW() - INTERVAL '%s days'
                GROUP BY DATE(created_at), emotion
                ORDER BY date, emotion
            """, days)
        
        timeline = {}
        for row in rows:
            date_str = row["date"].isoformat()
            if date_str not in timeline:
                timeline[date_str] = {}
            timeline[date_str][row["emotion"]] = row["count"]
        
        return {"timeline": timeline, "period_days": days}

    async def close(self):
        """Close database connections"""
        if self.db_pool:
            await self.db_pool.close()