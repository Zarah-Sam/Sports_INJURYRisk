"""
Risk Scoring Engine
Implements the exact weighted sports injury prediction formula specified:
Injury Risk Score =
    Biomechanical Deviations (35%) +
    Historical Injury Factors (20%) +
    Movement Asymmetry (20%) +
    Training Load Indicators (15%) +
    Fatigue Indicators (10%)
"""
from typing import Dict, Any, List
from backend.config import SCORING_WEIGHTS

class RiskScoringEngine:
    def __init__(self):
        self.weights = SCORING_WEIGHTS

    def compute_scores(
        self,
        biomech_summary: Dict[str, float],
        anomaly_summary: Dict[str, Any],
        athlete_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculates all sub-component scores and the composite weighted injury risk score.
        """
        # 1. Biomechanical Deviations (35%)
        # Influenced by Knee Valgus peak, low flexion stiff landing, and excessive trunk sway
        max_valgus = max(biomech_summary.get("knee_valgus_left", 0), biomech_summary.get("knee_valgus_right", 0))
        valgus_penalty = min(50.0, max(0.0, (max_valgus - 6.0) * 4.0)) # 0 at 6 deg, 40 at 16 deg
        
        avg_flex = (biomech_summary.get("knee_flexion_left", 60) + biomech_summary.get("knee_flexion_right", 60)) / 2.0
        stiff_landing_penalty = max(0.0, (40.0 - avg_flex) * 1.5) if avg_flex < 40.0 else 0.0

        trunk_penalty = min(25.0, biomech_summary.get("trunk_lateral_lean", 0) * 1.8)
        
        bio_dev_score = min(100.0, max(5.0, valgus_penalty + stiff_landing_penalty + trunk_penalty))

        # 2. Historical Injury Factors (20%)
        # Prior ACL, ligament repairs or chronic sprains increase re-injury hazard
        history = athlete_profile.get("injury_history", [])
        hist_score = 10.0 # baseline low
        for inj in history:
            text = (inj.get("injury") if isinstance(inj, dict) else str(inj)).lower()
            if "acl" in text or "cruciate" in text:
                hist_score += 45.0
            elif "hamstring" in text or "femoris" in text:
                hist_score += 30.0
            elif "ankle" in text or "sprain" in text:
                hist_score += 25.0
            elif "disc" in text or "lumbar" in text or "back" in text:
                hist_score += 30.0
            else:
                hist_score += 15.0
        hist_score = min(100.0, hist_score)

        # 3. Movement Asymmetry (20%)
        asym_pct = biomech_summary.get("bilateral_asymmetry_pct", 10.0)
        # >15% is clinically significant
        asym_score = min(100.0, max(5.0, asym_pct * 3.5))

        # 4. Training Load Indicators (15%)
        # ACWR (Acute:Chronic Workload Ratio): Sweet spot = 0.8 to 1.3. Danger zone >= 1.5
        t_load = athlete_profile.get("training_load", {})
        acwr = t_load.get("acwr", 1.1)
        if acwr > 1.5:
            # Danger spike
            load_score = min(100.0, 75.0 + (acwr - 1.5) * 60.0)
        elif acwr > 1.3:
            load_score = 45.0 + (acwr - 1.3) * 150.0
        elif acwr < 0.7:
            # Underprepared
            load_score = 40.0
        else:
            load_score = 20.0 # In the safe optimal zone

        # 5. Fatigue Indicators (10%)
        athlete_fatigue = t_load.get("fatigue_index", 40.0)
        drift_bonus = 25.0 if anomaly_summary.get("fatigue_degradation_detected") else 0.0
        fatigue_score = min(100.0, athlete_fatigue * 0.75 + drift_bonus)

        # COMPOSITE WEIGHTED INJURY RISK SCORE
        weighted_score = (
            bio_dev_score * self.weights["biomechanical_deviations"] +
            hist_score * self.weights["historical_injury_factors"] +
            asym_score * self.weights["movement_asymmetry"] +
            load_score * self.weights["training_load_indicators"] +
            fatigue_score * self.weights["fatigue_indicators"]
        )
        weighted_score = round(min(100.0, max(0.0, weighted_score)), 1)

        # Categorize
        if weighted_score <= 30.0:
            category = "Low Risk"
            category_color = "#10b981" # Green
        elif weighted_score <= 60.0:
            category = "Moderate Risk"
            category_color = "#f59e0b" # Amber
        elif weighted_score <= 80.0:
            category = "High Risk"
            category_color = "#f97316" # Orange
        else:
            category = "Critical Risk"
            category_color = "#ef4444" # Red

        # Auxiliary Scores
        movement_quality = round(max(10.0, 100.0 - (bio_dev_score * 0.55 + asym_score * 0.45)), 1)
        biomech_efficiency = round(max(15.0, 100.0 - (anomaly_summary.get("anomaly_score", 20.0) * 0.5 + fatigue_score * 0.5)), 1)
        athlete_health_score = round(max(20.0, 100.0 - weighted_score * 0.65), 1)

        return {
            "overall_risk_score": weighted_score,
            "risk_category": category,
            "category_color": category_color,
            "movement_quality_score": movement_quality,
            "biomechanical_efficiency_score": biomech_efficiency,
            "athlete_health_score": athlete_health_score,
            "weighted_breakdown": {
                "biomechanical_deviations": round(bio_dev_score, 1),
                "historical_injury_factors": round(hist_score, 1),
                "movement_asymmetry": round(asym_score, 1),
                "training_load_indicators": round(load_score, 1),
                "fatigue_indicators": round(fatigue_score, 1)
            },
            "formula_contributions": {
                "biomechanical_contribution": round(bio_dev_score * self.weights["biomechanical_deviations"], 2),
                "history_contribution": round(hist_score * self.weights["historical_injury_factors"], 2),
                "asymmetry_contribution": round(asym_score * self.weights["movement_asymmetry"], 2),
                "load_contribution": round(load_score * self.weights["training_load_indicators"], 2),
                "fatigue_contribution": round(fatigue_score * self.weights["fatigue_indicators"], 2)
            }
        }

# Singleton
risk_scorer = RiskScoringEngine()
