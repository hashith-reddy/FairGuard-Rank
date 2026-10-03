import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.matcher import compute_similarity, rank_candidates

def test_similarity():
    job_desc = "Looking for a Python backend developer with FastAPI experience."
    cand1 = "Experienced Python backend developer. Skilled in FastAPI and SQL."
    cand2 = "Frontend developer using React and CSS."
    
    score1 = compute_similarity(job_desc, cand1)
    score2 = compute_similarity(job_desc, cand2)
    
    # Ensure similarity with matching profile is higher than mismatching
    assert score1 > score2

def test_ranking():
    job_desc = "Looking for a Python backend developer with FastAPI experience."
    candidates = [
        {"id": 1, "text": "Frontend developer using React and CSS.", "name": "Alice"},
        {"id": 2, "text": "Experienced Python backend developer. Skilled in FastAPI and SQL.", "name": "Bob"}
    ]
    
    ranked = rank_candidates(job_desc, candidates)
    
    # Bob should be ranked higher than Alice
    assert ranked[0]["name"] == "Bob"
    assert ranked[1]["name"] == "Alice"
