import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.fairness import assess_fairness

def test_assess_fairness():
    # Mock data
    data = {
        'gender': [1, 1, 1, 0, 0, 0], # 1: privileged, 0: unprivileged
        'shortlisted': [1, 1, 0, 1, 0, 0] # 1: favorable, 0: unfavorable
    }
    df = pd.DataFrame(data)
    
    result = assess_fairness(df, 'gender', 'shortlisted')
    
    # Check if aif360 is available, if not it returns an error dict
    if "error" in result and result["error"] == "AIF360 not installed":
        assert True
    else:
        assert "spd" in result
        assert "disparate_impact" in result
