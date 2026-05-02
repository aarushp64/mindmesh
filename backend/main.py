from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime
import sys
import os
from dotenv import load_dotenv

# Add parent directory to sys.path to allow importing from ai-engine and database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Import our core modules from their new locations
from database.memory_engine import MemoryEngine
from ai_engine.ai_twin import AITwin
from ai_engine.thought_processor import ThoughtProcessor

app = FastAPI(
    title="MindMesh API",
    description="AI Digital Twin - Your mind, evolving beside you",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core engines
memory_engine = MemoryEngine()
ai_twin = AITwin()
thought_processor = ThoughtProcessor()

# Pydantic models for API requests/responses
class ThoughtInput(BaseModel):
    content: str
    thought_type: Optional[str] = "thought"  # thought, plan, memory, goal
    metadata: Optional[Dict[str, Any]] = {}

class ChatMessage(BaseModel):
    message: str
    context_limit: Optional[int] = 10

class ThoughtResponse(BaseModel):
    id: str
    content: str
    thought_type: str
    emotion: str
    timestamp: datetime
    embedding_created: bool

class ChatResponse(BaseModel):
    response: str
    context_memories: List[Dict[str, Any]]
    personality_insight: Optional[str] = None

class ReflectionSummary(BaseModel):
    period: str
    key_themes: List[str]
    emotional_patterns: Dict[str, Any]
    insights: List[str]
    suggested_actions: List[str]

@app.get("/")
async def root():
    return {"message": "MindMesh AI Twin - Your digital reflection awaits"}

@app.post("/thoughts", response_model=ThoughtResponse)
async def capture_thought(thought_input: ThoughtInput):
    """Capture and process a new thought, memory, plan, or goal"""
    try:
        # Process the thought (emotion detection, categorization)
        processed_thought = await thought_processor.process(
            content=thought_input.content,
            thought_type=thought_input.thought_type,
            metadata=thought_input.metadata
        )
        
        # Store in memory with vector embedding
        memory_id = await memory_engine.store_memory(
            content=processed_thought["content"],
            thought_type=processed_thought["type"],
            emotion=processed_thought["emotion"],
            metadata=processed_thought["metadata"]
        )
        
        # Update AI twin's personality model
        await ai_twin.update_personality(processed_thought)
        
        return ThoughtResponse(
            id=memory_id,
            content=processed_thought["content"],
            thought_type=processed_thought["type"],
            emotion=processed_thought["emotion"],
            timestamp=datetime.now(),
            embedding_created=True
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing thought: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_twin(chat_message: ChatMessage):
    """Chat with your AI twin - it responds with memory and personality context"""
    try:
        # Retrieve relevant memories based on the message
        relevant_memories = await memory_engine.retrieve_memories(
            query=chat_message.message,
            limit=chat_message.context_limit
        )
        
        # Generate response using AI twin with context
        response = await ai_twin.generate_response(
            message=chat_message.message,
            memories=relevant_memories
        )
        
        return ChatResponse(
            response=response["text"],
            context_memories=relevant_memories,
            personality_insight=response.get("personality_note")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@app.get("/memories")
async def get_memories(
    limit: int = 20,
    thought_type: Optional[str] = None,
    emotion: Optional[str] = None
):
    """Retrieve stored memories with optional filtering"""
    try:
        memories = await memory_engine.get_memories(
            limit=limit,
            thought_type=thought_type,
            emotion=emotion
        )
        return {"memories": memories}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving memories: {str(e)}")

@app.get("/personality")
async def get_personality_profile():
    """Get current personality model and insights"""
    try:
        profile = await ai_twin.get_personality_profile()
        return profile
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting personality: {str(e)}")

@app.get("/reflection/{period}")
async def get_reflection_summary(period: str):
    """Get automated reflection summary (daily, weekly, monthly)"""
    try:
        if period not in ["daily", "weekly", "monthly"]:
            raise HTTPException(status_code=400, detail="Period must be daily, weekly, or monthly")
        
        summary = await ai_twin.generate_reflection_summary(period)
        
        return ReflectionSummary(
            period=period,
            key_themes=summary["themes"],
            emotional_patterns=summary["emotions"],
            insights=summary["insights"],
            suggested_actions=summary["actions"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating reflection: {str(e)}")

@app.get("/mind-graph")
async def get_mind_graph():
    """Get graph data for mind visualization"""
    try:
        graph_data = await memory_engine.get_mind_graph()
        return {"nodes": graph_data["nodes"], "edges": graph_data["edges"]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating mind graph: {str(e)}")

@app.delete("/memories/{memory_id}")
async def delete_memory(memory_id: str):
    """Delete a specific memory"""
    try:
        await memory_engine.delete_memory(memory_id)
        return {"message": f"Memory {memory_id} deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting memory: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)