from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

model = None

def get_model():
    global model
    if model is None:
        try:
            model = SentenceTransformer(config.EMBEDDING_MODEL)
        except Exception as e:
            print(f"Warning: Could not load model {config.EMBEDDING_MODEL}: {e}")
    return model

def get_embedding(text: str):
    m = get_model()
    if not m:
        return np.zeros((384,))
    return m.encode(text)

def compute_similarity(job_desc: str, candidate_text: str) -> float:
    m = get_model()
    if not m:
        return 0.0
    
    job_emb = get_embedding(job_desc)
    cand_emb = get_embedding(candidate_text)
    
    # Cosine similarity requires 2D arrays
    similarity = cosine_similarity([job_emb], [cand_emb])[0][0]
    return float(max(0.0, similarity) * 100.0) # 0 to 100%

def rank_candidates(job_desc: str, candidates: list) -> list:
    """
    candidates is a list of dicts: [{"id": 1, "text": "...", "name": "..."}]
    """
    scored_candidates = []
    for cand in candidates:
        score = compute_similarity(job_desc, cand["text"])
        scored_candidates.append({
            **cand,
            "score": score
        })
        
    return sorted(scored_candidates, key=lambda x: x["score"], reverse=True)
