import asyncio
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class ThoughtProcessor:
    """Processes raw thoughts to extract meaning, emotion, and categorization"""
    
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Predefined emotion categories
        self.emotion_categories = [
            "excited", "hopeful", "content", "peaceful", "grateful", "inspired",
            "anxious", "frustrated", "sad", "angry", "overwhelmed", "confused",
            "curious", "motivated", "reflective", "nostalgic", "proud", "lonely",
            "determined", "creative", "doubtful", "energized", "contemplative", "neutral"
        ]
        
        # Thought type patterns for quick classification
        self.thought_patterns = {
            "goal": ["want to", "goal", "aspire", "achieve", "dream", "hope to", "aim"],
            "plan": ["will", "going to", "plan", "schedule", "tomorrow", "next", "organize"],
            "memory": ["remember", "used to", "back when", "in the past", "recall", "reminds me"],
            "reflection": ["feel", "think", "realize", "understand", "learned", "noticed"]
        }
    
    async def process(
        self, 
        content: str, 
        thought_type: str = "thought", 
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process a raw thought and extract structured information"""
        
        # Clean and normalize content
        cleaned_content = self._clean_content(content)
        
        # Auto-detect thought type if not specified or is generic
        if thought_type == "thought" or not thought_type:
            thought_type = await self._classify_thought_type(cleaned_content)
        
        # Detect emotion
        emotion = await self._detect_emotion(cleaned_content, thought_type)
        
        # Extract key themes and topics
        themes = await self._extract_themes(cleaned_content)
        
        # Build metadata
        processed_metadata = metadata or {}
        processed_metadata.update({
            "themes": themes,
            "word_count": len(cleaned_content.split()),
            "processed_at": datetime.now().isoformat(),
            "has_question": "?" in cleaned_content,
            "urgency": self._detect_urgency(cleaned_content)
        })
        
        return {
            "content": cleaned_content,
            "type": thought_type,
            "emotion": emotion,
            "metadata": processed_metadata
        }
    
    def _clean_content(self, content: str) -> str:
        """Clean and normalize thought content"""
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content.strip())
        
        # Basic cleanup
        content = content.replace('\n', ' ').replace('\r', ' ')
        
        return content
    
    async def _classify_thought_type(self, content: str) -> str:
        """Classify the type of thought using patterns and LLM"""
        
        # Quick pattern-based classification first
        content_lower = content.lower()
        for thought_type, patterns in self.thought_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                return thought_type
        
        # If no patterns match, use LLM for classification
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """Classify this thought into ONE of these categories:
                        - thought: general reflection, observation, or idea
                        - plan: intention, schedule, or future action
                        - memory: recollection of past events or experiences
                        - goal: aspiration, desire, or long-term objective
                        
                        Return only the category name, nothing else."""
                    },
                    {"role": "user", "content": content}
                ],
                temperature=0.1,
                max_tokens=10
            )
            
            classification = response.choices[0].message.content.strip().lower()
            
            # Validate classification
            valid_types = ["thought", "plan", "memory", "goal"]
            return classification if classification in valid_types else "thought"
            
        except Exception as e:
            print(f"Error in thought classification: {e}")
            return "thought"  # Default fallback
    
    async def _detect_emotion(self, content: str, thought_type: str) -> str:
        """Detect the emotional tone of the thought"""
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"""Analyze the emotional tone of this {thought_type}. 
                        
                        Choose the BEST fitting emotion from this list:
                        {', '.join(self.emotion_categories)}
                        
                        Consider:
                        - The overall sentiment and mood
                        - Intensity of language used
                        - Context of the thought type
                        
                        Return only the emotion name, nothing else."""
                    },
                    {"role": "user", "content": content}
                ],
                temperature=0.2,
                max_tokens=15
            )
            
            emotion = response.choices[0].message.content.strip().lower()
            
            # Validate emotion is in our categories
            return emotion if emotion in self.emotion_categories else "neutral"
            
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            return self._fallback_emotion_detection(content)
    
    def _fallback_emotion_detection(self, content: str) -> str:
        """Simple rule-based emotion detection as fallback"""
        content_lower = content.lower()
        
        # Positive emotions
        if any(word in content_lower for word in ["excited", "happy", "love", "amazing", "great"]):
            return "excited"
        elif any(word in content_lower for word in ["hope", "dream", "aspire", "looking forward"]):
            return "hopeful"
        elif any(word in content_lower for word in ["grateful", "thankful", "blessed"]):
            return "grateful"
        
        # Negative emotions
        elif any(word in content_lower for word in ["worry", "anxious", "stress", "nervous"]):
            return "anxious"
        elif any(word in content_lower for word in ["sad", "down", "depressed", "upset"]):
            return "sad"
        elif any(word in content_lower for word in ["angry", "frustrated", "annoyed", "mad"]):
            return "frustrated"
        
        # Neutral/contemplative
        elif any(word in content_lower for word in ["think", "wonder", "consider", "reflect"]):
            return "reflective"
        
        return "neutral"
    
    async def _extract_themes(self, content: str) -> List[str]:
        """Extract key themes and topics from the thought"""
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """Extract 2-4 key themes or topics from this thought. 
                        
                        Return them as single words or short phrases (2-3 words max).
                        Examples: "creativity", "work stress", "relationships", "personal growth"
                        
                        Return as a comma-separated list, nothing else."""
                    },
                    {"role": "user", "content": content}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            themes_text = response.choices[0].message.content.strip()
            themes = [theme.strip().lower() for theme in themes_text.split(",")]
            
            # Filter out empty themes and limit to 5
            return [theme for theme in themes if theme and len(theme) > 1][:5]
            
        except Exception as e:
            print(f"Error extracting themes: {e}")
            return ["general"]  # Fallback theme
    
    def _detect_urgency(self, content: str) -> str:
        """Detect urgency level of the thought"""
        content_lower = content.lower()
        
        # High urgency indicators
        urgent_words = ["urgent", "asap", "immediately", "now", "today", "deadline", "emergency"]
        if any(word in content_lower for word in urgent_words):
            return "high"
        
        # Medium urgency indicators
        medium_words = ["soon", "this week", "important", "need to", "should"]
        if any(word in content_lower for word in medium_words):
            return "medium"
        
        # Questions often indicate some urgency
        if "?" in content:
            return "medium"
        
        return "low"
    
    async def analyze_batch(self, thoughts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze a batch of thoughts for patterns and insights"""
        
        if not thoughts:
            return {"insights": [], "patterns": {}}
        
        # Process all thoughts
        processed_thoughts = []
        for thought_data in thoughts:
            processed = await self.process(
                content=thought_data["content"],
                thought_type=thought_data.get("thought_type", "thought"),
                metadata=thought_data.get("metadata", {})
            )
            processed_thoughts.append(processed)
        
        # Analyze patterns
        emotion_counts = {}
        theme_counts = {}
        type_counts = {}
        
        for thought in processed_thoughts:
            # Count emotions
            emotion = thought["emotion"]
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            # Count themes
            for theme in thought["metadata"]["themes"]:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
            
            # Count types
            thought_type = thought["type"]
            type_counts[thought_type] = type_counts.get(thought_type, 0) + 1
        
        # Generate insights
        insights = []
        
        # Most common emotion
        if emotion_counts:
            top_emotion = max(emotion_counts, key=emotion_counts.get)
            insights.append(f"Most frequent emotion: {top_emotion} ({emotion_counts[top_emotion]} times)")
        
        # Most common theme
        if theme_counts:
            top_theme = max(theme_counts, key=theme_counts.get)
            insights.append(f"Most discussed theme: {top_theme} ({theme_counts[top_theme]} times)")
        
        # Thought type distribution
        if type_counts:
            top_type = max(type_counts, key=type_counts.get)
            insights.append(f"Primary thought type: {top_type} ({type_counts[top_type]} times)")
        
        return {
            "insights": insights,
            "patterns": {
                "emotions": emotion_counts,
                "themes": theme_counts,
                "types": type_counts
            },
            "processed_thoughts": processed_thoughts
        }