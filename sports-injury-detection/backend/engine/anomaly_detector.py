"""
Movement Anomaly & Fatigue Detection Engine
Analyzes kinematic trajectories over time to identify movement deviations,
technique inconsistency, and fatigue-induced motor control degradation.
"""
import numpy as np
from typing import List, Dict, Any

class MovementAnomalyDetector:
    def __init__(self):
        pass

    def detect_anomalies(self, frame_metrics_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes a sequence of frame-level biomechanical metrics.
        Returns anomaly scores, fatigue index, and detected deviations.
        """
        if not frame_metrics_history or len(frame_metrics_history) < 5:
            return {
                "anomaly_score": 15.0,
                "fatigue_degradation_detected": False,
                "technique_consistency_score": 88.0,
                "deviations": []
            }

        n_frames = len(frame_metrics_history)
        valgus_l = [m["knee_valgus_left"] for m in frame_metrics_history]
        valgus_r = [m["knee_valgus_right"] for m in frame_metrics_history]
        trunk_lean = [m["trunk_lateral_lean"] for m in frame_metrics_history]
        hip_drop = [m["hip_stability_drop"] for m in frame_metrics_history]

        # 1. Variance and Inconsistency
        std_valgus = float(np.std(valgus_l) + np.std(valgus_r)) / 2.0
        std_trunk = float(np.std(trunk_lean))
        
        # 2. Fatigue Drift Analysis (First third vs Last third of repetitions)
        third = max(1, n_frames // 3)
        early_valgus = np.mean(valgus_l[:third])
        late_valgus = np.mean(valgus_l[-third:])
        valgus_drift = late_valgus - early_valgus

        early_trunk = np.mean(trunk_lean[:third])
        late_trunk = np.mean(trunk_lean[-third:])
        trunk_drift = late_trunk - early_trunk

        fatigue_detected = False
        fatigue_notes = []

        if valgus_drift > 3.0:
            fatigue_detected = True
            fatigue_notes.append(f"Knee valgus increased by +{round(valgus_drift, 1)}° under fatigue loading")

        if trunk_drift > 2.5:
            fatigue_detected = True
            fatigue_notes.append(f"Torso lateral sway widened by +{round(trunk_drift, 1)}° indicating core exhaustion")

        # 3. Aggregate Anomaly Score (0 to 100)
        base_instability = (std_valgus * 4.0) + (std_trunk * 3.0) + (float(np.mean(hip_drop)) * 2.0)
        fatigue_penalty = 20.0 if fatigue_detected else 0.0
        anomaly_score = min(100.0, max(5.0, base_instability + fatigue_penalty))

        # Technique consistency (100 is robotic perfection)
        consistency = max(20.0, 100.0 - (std_valgus * 5.0 + std_trunk * 4.0))

        deviations = []
        if max(valgus_l) > 14.0 or max(valgus_r) > 14.0:
            deviations.append("Acute Knee Abduction Moment (Valgus Peak Spike)")
        if max(hip_drop) > 9.0:
            deviations.append("Pelvic Lateral Unleveling Spike (Gluteal Dropout)")
        if fatigue_detected:
            deviations.extend(fatigue_notes)

        return {
            "anomaly_score": round(anomaly_score, 1),
            "fatigue_degradation_detected": fatigue_detected,
            "technique_consistency_score": round(consistency, 1),
            "valgus_drift_deg": round(float(valgus_drift), 1),
            "deviations": deviations
        }

# Singleton
anomaly_detector = MovementAnomalyDetector()
