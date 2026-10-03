import shap
import numpy as np
import matplotlib.pyplot as plt
import io
import pandas as pd
from sklearn.linear_model import LinearRegression

def analyze_skill_gap(candidate_skills: list, required_skills: list) -> dict:
    """
    Identify missing and matched skills.
    """
    candidate_skills_set = set([s.lower() for s in candidate_skills])
    required_skills_set = set([s.lower() for s in required_skills])
    
    matched = list(candidate_skills_set.intersection(required_skills_set))
    missing = list(required_skills_set.difference(candidate_skills_set))
    extra = list(candidate_skills_set.difference(required_skills_set))
    
    match_percentage = len(matched) / len(required_skills_set) if required_skills_set else 1.0
    
    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "match_percentage": match_percentage
    }

def generate_shap_explanation(candidate_skills: list, required_skills: list):
    """
    Use a surrogate model (Linear Regression) to explain skill drivers.
    Returns top-5 positive skill drivers and top-5 missing skill penalties, and a plot.
    """
    if not required_skills:
        return None
        
    # Create feature space based on required skills
    features = [s.lower() for s in required_skills]
    
    # Synthetic background data (random combination of skills presence)
    np.random.seed(42)
    X_background = np.random.randint(0, 2, size=(100, len(features)))
    
    # Surrogate model: simple weighted sum (just for SHAP to have something to explain)
    weights = np.random.uniform(0.5, 1.5, size=len(features))
    y_background = np.dot(X_background, weights)
    
    model = LinearRegression()
    model.fit(X_background, y_background)
    
    explainer = shap.LinearExplainer(model, X_background)
    
    # Candidate data vector
    candidate_skills_lower = [s.lower() for s in candidate_skills]
    x_candidate = np.array([[1 if f in candidate_skills_lower else 0 for f in features]])
    
    shap_values = explainer.shap_values(x_candidate)
    
    # Identify drivers
    drivers = []
    for i, feature in enumerate(features):
        drivers.append((feature, shap_values[0][i]))
        
    drivers.sort(key=lambda x: x[1], reverse=True)
    
    positive_drivers = [d for d in drivers if d[1] > 0][:5]
    negative_penalties = [d for d in drivers if d[1] <= 0][:5]
    negative_penalties.sort(key=lambda x: x[1]) # Most negative first
    
    # Create plot
    plt.figure(figsize=(8, max(4, len(features)*0.5)))
    
    shap.summary_plot(shap_values, x_candidate, feature_names=features, plot_type="bar", show=False)
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    return {
        "positive_drivers": positive_drivers,
        "negative_penalties": negative_penalties,
        "plot_bytes": buf.getvalue()
    }
