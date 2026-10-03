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
    
    # Expanded tech skills dictionary for robust NER
    tech_skills = [
        # Languages
        'python', 'java', 'c++', 'c#', 'c', 'javascript', 'typescript', 'go', 'golang', 'rust', 'ruby', 'php', 'swift', 'kotlin', 'r', 'matlab', 'scala', 'dart', 'html', 'css', 'bash', 'shell', 'perl',
        # ML & AI
        'machine learning', 'deep learning', 'ai', 'artificial intelligence', 'nlp', 'computer vision', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'scipy', 'opencv', 'huggingface', 'llm', 'genai',
        # Backend & Web
        'sql', 'nosql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'elasticsearch', 'fastapi', 'flask', 'django', 'spring boot', 'express', 'node.js', 'nodejs', 'graphql', 'rest api',
        # Frontend
        'react', 'angular', 'vue', 'vue.js', 'next.js', 'svelte', 'tailwind', 'bootstrap', 'jquery',
        # DevOps & Cloud
        'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'k8s', 'terraform', 'ansible', 'jenkins', 'github actions', 'ci/cd', 'linux', 'ubuntu', 'git', 'bitbucket',
        # Big Data
        'hadoop', 'spark', 'kafka', 'airflow', 'snowflake', 'databricks', 'tableau', 'power bi'
    ]
    
    # Check for skills using word boundaries to avoid partial matches
    text_lower = text.lower()
    for skill in tech_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            skills.append(skill)
            
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
