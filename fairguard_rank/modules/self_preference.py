def evaluate_self_preference(human_text_score: float, ai_text_score: float) -> dict:
    """
    Compare the score of a human-written resume to an AI-rewritten version.
    Returns metrics indicating potential AI self-preference bias.
    """
    score_diff = ai_text_score - human_text_score
    
    # Positive score difference indicates the model preferred the AI text
    preference_bias = score_diff > 0.05
    
    return {
        "human_score": human_text_score,
        "ai_score": ai_text_score,
        "score_difference": score_diff,
        "ai_preference_detected": preference_bias,
        "insight": "AI preference detected. The model ranked the LLM-generated text significantly higher." if preference_bias else "No significant AI preference detected."
    }
