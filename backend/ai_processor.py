"""
AI-powered note processing module for extracting titles, tags, and finding connections.
"""
import re
from typing import List, Tuple, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer, util

def extract_title(text: str) -> str:
    """Extract a title from the text content."""
    # Split into sentences and get the first meaningful one
    sentences = text.split('.')
    first_sentence = sentences[0].strip()
    
    # If the first sentence is too long, try to extract key phrase
    if len(first_sentence) > 50:
        # Take first phrase or limit to 50 chars
        phrases = first_sentence.split(',')
        title = phrases[0].strip()
        return title[:50] + ('...' if len(title) > 50 else '')
    
    return first_sentence

def extract_tags(text: str, model: SentenceTransformer) -> List[str]:
    """Extract relevant tags from the text using AI."""
    # Common topic categories
    predefined_tags = {
        "tech": ["programming", "software", "technology", "computer", "coding", "development", "app", "web"],
        "business": ["strategy", "management", "marketing", "finance", "startup", "business", "product"],
        "creativity": ["design", "art", "writing", "ideas", "creative", "innovation", "brainstorm"],
        "learning": ["study", "education", "learning", "knowledge", "research", "understanding"],
        "productivity": ["workflow", "efficiency", "organization", "planning", "productivity", "time"],
        "personal": ["reflection", "thoughts", "goals", "personal", "life", "motivation"]
    }
    
    # Encode the text
    text_embedding = model.encode(text, normalize_embeddings=True)
    
    # Find relevant tags
    tags = set()
    for category, keywords in predefined_tags.items():
        # Encode keywords
        keyword_embeddings = model.encode(keywords, normalize_embeddings=True)
        
        # Calculate similarities
        similarities = util.dot_score(text_embedding, keyword_embeddings)[0]
        
        # If any keyword is similar enough, add the category
        if np.max(similarities) > 0.3:
            tags.add(category)
            
            # Add the most relevant keyword
            most_relevant = keywords[np.argmax(similarities)]
            tags.add(most_relevant)
    
    # Extract potential technical terms or key phrases
    words = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b', text)  # CamelCase words
    tags.update(word.lower() for word in words)
    
    return list(tags)

def find_similar_notes(text: str, notes: List[Dict[str, Any]], model: SentenceTransformer, 
                      threshold: float = 0.5) -> List[Tuple[int, float]]:
    """Find similar existing notes using semantic similarity."""
    if not notes:
        return []
        
    # Encode the new text
    text_embedding = model.encode(text, normalize_embeddings=True)
    
    similar_notes = []
    for note in notes:
        if not note.get('embedding'):
            continue
            
        # Calculate similarity
        note_embedding = np.array(note['embedding'])
        similarity = float(util.dot_score(text_embedding, note_embedding)[0][0])
        
        if similarity > threshold:
            similar_notes.append((note['id'], similarity))
    
    # Sort by similarity score
    similar_notes.sort(key=lambda x: x[1], reverse=True)
    return similar_notes

def process_raw_note(content: str, existing_notes: List[Dict[str, Any]], 
                    model: SentenceTransformer) -> Dict[str, Any]:
    """Process raw note content into a structured note with AI-generated metadata."""
    # Extract title from the first sentence or key phrase
    title = extract_title(content)
    
    # Generate tags using AI
    tags = extract_tags(content, model)
    
    # Find similar notes for automatic linking
    similar_notes = find_similar_notes(content, existing_notes, model)
    link_ids = [id for id, score in similar_notes if score > 0.6]  # Only link highly similar notes
    
    # Generate embedding for the complete note
    text_for_embedding = f"{title}\n{content}"
    embedding = model.encode(text_for_embedding, normalize_embeddings=True).tolist()
    
    return {
        "title": title,
        "content": content,
        "tags": tags,
        "link_ids": link_ids,
        "embedding": embedding
    }