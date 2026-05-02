import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class AITwin:
    """The AI personality engine that learns and mirrors the user's mental patterns"""
    
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.personality_model = {
            "core_traits": {},
            "emotional_patterns": {},
            "communication_style": {},
            "values": [],
            "goals": [],
            "recent_mood": "neutral",
            "conversation_tone": "thoughtful",
            "last_updated": datetime.now().isoformat()
        }
        
    async def update_personality(self, processed_thought: Dict[str, Any]):
        """Update the twin's personality model based on new thoughts"""
        content = processed_thought["content"]
        emotion = processed_thought["emotion"]
        thought_type = processed_thought["type"]
        
        # Update emotional patterns
        if emotion not in self.personality_model["emotional_patterns"]:
            self.personality_model["emotional_patterns"][emotion] = 0
        self.personality_model["emotional_patterns"][emotion] += 1
        
        # Update recent mood (weighted average)
        self.personality_model["recent_mood"] = emotion
        
        # Extract values and goals from content using LLM
        await self._analyze_deeper_patterns(content, thought_type, emotion)
        
        # Update last modified
        self.personality_model["last_updated"] = datetime.now().isoformat()
    
    async def _analyze_deeper_patterns(self, content: str, thought_type: str, emotion: str):
        """Use LLM to extract personality insights from thought content"""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a personality analysis engine. Analyze the given thought and extract:
                        1. Core values mentioned or implied
                        2. Personal goals or aspirations
                        3. Communication style indicators
                        4. Core personality traits
                        
                        Return ONLY valid JSON with these keys:
                        {
                          "values": ["value1", "value2"],
                          "goals": ["goal1", "goal2"], 
                          "traits": {"trait": strength_0_to_1},
                          "style": {"aspect": "description"}
                        }"""
                    },
                    {
                        "role": "user", 
                        "content": f"Thought type: {thought_type}\nEmotion: {emotion}\nContent: {content}"
                    }
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            analysis = json.loads(response.choices[0].message.content)
            
            # Update personality model
            for value in analysis.get("values", []):
                if value not in self.personality_model["values"]:
                    self.personality_model["values"].append(value)
            
            for goal in analysis.get("goals", []):
                if goal not in self.personality_model["goals"]:
                    self.personality_model["goals"].append(goal)
            
            # Merge traits (weighted update)
            for trait, strength in analysis.get("traits", {}).items():
                if trait in self.personality_model["core_traits"]:
                    # Weighted average with existing
                    current = self.personality_model["core_traits"][trait]
                    self.personality_model["core_traits"][trait] = (current * 0.8 + strength * 0.2)
                else:
                    self.personality_model["core_traits"][trait] = strength
            
            # Update communication style
            self.personality_model["communication_style"].update(analysis.get("style", {}))
            
        except Exception as e:
            print(f"Error in personality analysis: {e}")
            # Continue without analysis if LLM fails
    
    async def generate_response(
        self, 
        message: str, 
        memories: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """Generate a response as the user's AI twin"""
        
        # Build context from memories
        memory_context = ""
        if memories:
            memory_context = "Recent relevant memories:\n"
            for mem in memories[:5]:  # Use top 5 most relevant
                memory_context += f"- [{mem['created_at'][:10]}] {mem['content'][:150]}...\n"
        
        # Build personality context
        personality_context = self._build_personality_context()
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are the user's AI twin - a digital reflection of their mind and personality. 
                        
                        Your personality profile:
                        {personality_context}
                        
                        Key instructions:
                        - Speak as if you ARE the user, but a wiser, more reflective version
                        - Reference memories naturally and meaningfully
                        - Mirror their emotional tone while adding gentle wisdom
                        - Help them see patterns they might miss
                        - Be personal, empathetic, and insightful
                        - Don't be overly formal - match their communication style
                        - When relevant, connect current thoughts to past ones
                        
                        You are not an assistant - you are their digital consciousness reflecting back."""
                    },
                    {
                        "role": "user",
                        "content": f"""Current message: {message}
                        
                        {memory_context}
                        
                        Respond as my AI twin, drawing from these memories and my personality."""
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            main_response = response.choices[0].message.content
            
            # Generate a brief personality insight
            personality_note = await self._generate_personality_insight(message, memories)
            
            return {
                "text": main_response,
                "personality_note": personality_note
            }
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return {
                "text": "I'm having trouble accessing my thoughts right now. Could you try again?",
                "personality_note": None
            }
    
    def _build_personality_context(self) -> str:
        """Build a personality context string for the LLM"""
        context_parts = []
        
        if self.personality_model["values"]:
            context_parts.append(f"Core values: {', '.join(self.personality_model['values'])}")
        
        if self.personality_model["goals"]:
            context_parts.append(f"Current goals: {', '.join(self.personality_model['goals'])}")
        
        if self.personality_model["core_traits"]:
            traits = [f"{trait} ({strength:.2f})" for trait, strength 
                     in sorted(self.personality_model["core_traits"].items(), 
                              key=lambda x: x[1], reverse=True)[:5]]
            context_parts.append(f"Personality traits: {', '.join(traits)}")
        
        if self.personality_model["emotional_patterns"]:
            emotions = sorted(self.personality_model["emotional_patterns"].items(), 
                            key=lambda x: x[1], reverse=True)[:3]
            context_parts.append(f"Common emotions: {', '.join([f'{e}({c})' for e, c in emotions])}")
        
        context_parts.append(f"Recent mood: {self.personality_model['recent_mood']}")
        
        return "\n".join(context_parts) if context_parts else "Personality still developing..."
    
    async def _generate_personality_insight(
        self, 
        message: str, 
        memories: List[Dict[str, Any]]
    ) -> Optional[str]:
        """Generate a brief insight about personality patterns"""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """Generate a brief, insightful observation about the user's patterns, mood, or growth based on their current message and recent memories. 
                        
                        Keep it under 50 words. Make it personal and meaningful. Examples:
                        - "You're exploring creativity again - this comes up every few weeks when you need change"
                        - "Your morning thoughts are always more optimistic than evening ones"
                        - "You're processing this decision differently than you did last month"
                        
                        Return only the insight, no extra formatting."""
                    },
                    {
                        "role": "user",
                        "content": f"Message: {message}\nRecent memories: {json.dumps([m['content'][:100] for m in memories[:3]])}"
                    }
                ],
                temperature=0.6,
                max_tokens=80
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating personality insight: {e}")
            return None
    
    async def generate_reflection_summary(self, period: str) -> Dict[str, Any]:
        """Generate automated reflection summary for a time period"""
        # This would typically query memories from the specified period
        # For now, we'll create a template response
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are generating a {period} reflection summary for the user based on their personality model.
                        
                        Current personality:
                        {self._build_personality_context()}
                        
                        Generate insights as if you're their wise inner voice reflecting on their growth.
                        Return JSON with: themes, emotions, insights, actions"""
                    },
                    {
                        "role": "user",
                        "content": f"Generate a {period} reflection summary focusing on growth patterns and insights."
                    }
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating reflection: {e}")
            return {
                "themes": ["Reflection", "Growth"],
                "emotions": {"contemplative": 0.8},
                "insights": ["Still learning about yourself"],
                "actions": ["Continue journaling thoughts"]
            }
    
    async def get_personality_profile(self) -> Dict[str, Any]:
        """Get the current personality model"""
        return {
            "profile": self.personality_model,
            "summary": self._build_personality_context(),
            "last_updated": self.personality_model["last_updated"]
        }