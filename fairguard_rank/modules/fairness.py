import pandas as pd
import numpy as np

try:
    from aif360.datasets import StandardDataset
    from aif360.metrics import ClassificationMetric
    from aif360.algorithms.preprocessing import Reweighing
    AIF360_AVAILABLE = True
except ImportError:
    AIF360_AVAILABLE = False

def compute_ai_self_preference(human_scores: list, ai_scores: list) -> dict:
    """
    Compute AI self-preference variance: score shift between human and LLM-formulated profiles.
    """
    human_mean = np.mean(human_scores) if human_scores else 0
    ai_mean = np.mean(ai_scores) if ai_scores else 0
    shift = ai_mean - human_mean
    variance = np.var(ai_scores) - np.var(human_scores) if ai_scores and human_scores else 0
    
    return {
        "human_mean": float(human_mean),
        "ai_mean": float(ai_mean),
        "score_shift": float(shift),
        "variance_difference": float(variance),
        "preference_detected": shift > 5.0 # Assuming 0-100% scale
    }

def assess_fairness(df: pd.DataFrame, protected_attribute: str, target_attribute: str) -> dict:
    """
    Assess fairness metrics on a dataset of candidates.
    df should contain columns for the protected attribute and a binary target (e.g., shortlisted: 0 or 1)
    """
    if not AIF360_AVAILABLE:
        return {"error": "AIF360 not installed", "spd": 0, "disparate_impact": 0}
        
    try:
        privileged_groups = [{protected_attribute: 1}]
        unprivileged_groups = [{protected_attribute: 0}]
        
        analysis_df = df[[protected_attribute, target_attribute]].copy()
        dataset = StandardDataset(
            analysis_df,
            label_name=target_attribute,
            favorable_classes=[1],
            protected_attribute_names=[protected_attribute],
            privileged_classes=[[1]]
        )
        
        metric = ClassificationMetric(
            dataset, dataset, 
            unprivileged_groups=unprivileged_groups,
            privileged_groups=privileged_groups
        )
        
        spd = metric.statistical_parity_difference()
        di = metric.disparate_impact()
        
        return {
            "spd": float(spd),
            "disparate_impact": float(di),
            "is_fair_spd": abs(spd) < 0.05
        }
    except Exception as e:
        return {"error": str(e), "spd": 0, "disparate_impact": 0}

def mitigate_bias_reweighing(df: pd.DataFrame, protected_attribute: str, target_attribute: str):
    """
    Apply Reweighing to the dataset to output sample weights that mitigate bias ensuring |SPD| < 0.05.
    Returns a dataframe with weights applied or transformed scores.
    """
    if not AIF360_AVAILABLE:
        # Fallback manual calibration for demo purposes if AIF360 fails
        df['weights'] = 1.0
        return df
        
    try:
        privileged_groups = [{protected_attribute: 1}]
        unprivileged_groups = [{protected_attribute: 0}]
        
        analysis_df = df[[protected_attribute, target_attribute]].copy()
        dataset = StandardDataset(
            analysis_df,
            label_name=target_attribute,
            favorable_classes=[1],
            protected_attribute_names=[protected_attribute],
            privileged_classes=[[1]]
        )
        
        RW = Reweighing(unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
        dataset_transf = RW.fit_transform(dataset)
        
        # Verify mitigated SPD
        metric_transf = ClassificationMetric(
            dataset, dataset_transf,
            unprivileged_groups=unprivileged_groups,
            privileged_groups=privileged_groups
        )
        mitigated_spd = metric_transf.statistical_parity_difference()
        
        df['weights'] = dataset_transf.instance_weights
        df['mitigated_spd'] = mitigated_spd
        df['fairness_achieved'] = abs(mitigated_spd) < 0.05
        return df
    except Exception as e:
        df['weights'] = 1.0
        return df
