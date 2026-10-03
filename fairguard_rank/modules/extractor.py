import spacy
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

# Need to download spacy model in the environment: python -m spacy download en_core_web_sm
try:
    nlp = spacy.load(config.SPACY_MODEL)
except OSError:
    print(f"Warning: {config.SPACY_MODEL} not found. Please download it using: python -m spacy download {config.SPACY_MODEL}")
    nlp = None

def extract_entities(text: str) -> dict:
    if not nlp:
        return {"skills": [], "education": [], "experience_years": 0}
        
    doc = nlp(text)
    
    # Very basic heuristics for demo purposes
    skills = []
    education = []
    
    # Custom simple lists for demo
    tech_skills = ['python', 'java', 'c++', 'machine learning', 'ai', 'sql', 'fastapi', 'react', 'aws']
    
    for token in doc:
        if token.text.lower() in tech_skills:
            skills.append(token.text.lower())
            
    for ent in doc.ents:
        if ent.label_ == "ORG" and any(word in ent.text.lower() for word in ["university", "college", "institute"]):
            education.append(ent.text)
            
    # Regex for years of experience
    exp_years = 0
    exp_matches = re.findall(r'(\d+)\+?\s*(years?|yrs?)\s+of\s+experience', text.lower())
    if exp_matches:
        try:
            exp_years = max([int(m[0]) for m in exp_matches])
        except:
            pass
            
    return {
        "skills": list(set(skills)),
        "education": list(set(education)),
        "experience_years": exp_years
    }
