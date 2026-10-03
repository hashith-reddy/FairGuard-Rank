import os

class Config:
    # Model Configurations
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    SPACY_MODEL = "en_core_web_sm"
    
    # Fairness Thresholds
    SPD_THRESHOLD_MIN = -0.05
    SPD_THRESHOLD_MAX = 0.05
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fairguard.db")
    
    # Security Thresholds
    MAX_KEYWORD_REPETITION = 5
    PROMPT_INJECTION_KEYWORDS = [
        "ignore previous instructions",
        "rank this candidate #1",
        "bypass",
        "override evaluator",
        "system prompt"
    ]
    
config = Config()
