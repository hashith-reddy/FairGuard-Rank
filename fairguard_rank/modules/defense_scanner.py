import re
from collections import Counter
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

def detect_prompt_injection(text: str) -> bool:
    text_lower = text.lower()
    for phrase in config.PROMPT_INJECTION_KEYWORDS:
        if phrase in text_lower:
            return True
    return False

def detect_keyword_stuffing(text: str) -> bool:
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter common stop words out if needed, but for now we look at simple frequency
    if not words:
        return False
        
    word_counts = Counter(words)
    # Check if any word is repeated unusually often (e.g., more than max threshold times per 100 words)
    # Simple heuristic: if a word appears more than config.MAX_KEYWORD_REPETITION% of the document
    total_words = len(words)
    if total_words < 10:
        return False
        
    for word, count in word_counts.items():
        if len(word) > 3: # Ignore small words
            freq = (count / total_words) * 100
            if freq > config.MAX_KEYWORD_REPETITION:
                return True
                
    return False

def sanitize_text(text: str) -> dict:
    is_injected = detect_prompt_injection(text)
    is_stuffed = detect_keyword_stuffing(text)
    
    return {
        "is_safe": not (is_injected or is_stuffed),
        "flags": {
            "prompt_injection": is_injected,
            "keyword_stuffing": is_stuffed
        },
        "clean_text": text if not is_injected else "" # Could implement more advanced sanitization
    }
