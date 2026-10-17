"""
Biomechanical Analysis Engine
Computes joint angles, Knee Valgus, Trunk Lean, Hip Stability, Bilateral Symmetry,
and Landing Mechanics based on computer vision keypoint coordinates.
"""
import math
import numpy as np
from typing import Dict, Any, Tuple, Optional
from backend.config import THRESHOLDS

def calculate_angle_2d(p_a: Tuple[float, float], p_b: Tuple[float, float], p_c: Tuple[float, float]) -> float:
    """
    Calculates angle at vertex p_b formed by segments (p_a - p_b) and (p_c - p_b) in degrees [0, 180].
    """
    ba = (p_a[0] - p_b[0], p_a[1] - p_b[1])
    bc = (p_c[0] - p_b[0], p_c[1] - p_b[1])
    
    dot_prod = ba[0] * bc[0] + ba[1] * bc[1]
    mag_ba = math.hypot(ba[0], ba[1])
    mag_bc = math.hypot(bc[0], bc[1])
    
    if mag_ba < 1e-6 or mag_bc < 1e-6:
        return 180.0
        
    cos_angle = dot_prod / (mag_ba * mag_bc)
    cos_angle = max(-1.0, min(1.0, cos_angle))
    return math.degrees(math.acos(cos_angle))

class BiomechanicsAnalyzer:
    def __init__(self):
        self.thresholds = THRESHOLDS

    def analyze_frame(self, keypoints: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """
        Extracts comprehensive biomechanical telemetry for a single frame.
        """
        metrics = {
            "knee_valgus_left": 0.0,
            "knee_valgus_right": 0.0,
            "knee_flexion_left": 180.0,
            "knee_flexion_right": 180.0,
            "trunk_forward_lean": 0.0,
            "trunk_lateral_lean": 0.0,
            "hip_stability_drop": 0.0,
            "bilateral_asymmetry_pct": 0.0,
            "landing_force_proxy_g": 1.0,
            "flags": []
        }

        required_kpts = ["left_hip", "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle", "left_shoulder", "right_shoulder"]
        if not all(k in keypoints for k in required_kpts):
            return metrics

        l_hip = (keypoints["left_hip"]["x"], keypoints["left_hip"]["y"])
        r_hip = (keypoints["right_hip"]["x"], keypoints["right_hip"]["y"])
        l_knee = (keypoints["left_knee"]["x"], keypoints["left_knee"]["y"])
        r_knee = (keypoints["right_knee"]["x"], keypoints["right_knee"]["y"])
        l_ankle = (keypoints["left_ankle"]["x"], keypoints["left_ankle"]["y"])
        r_ankle = (keypoints["right_ankle"]["x"], keypoints["right_ankle"]["y"])
        l_sh = (keypoints["left_shoulder"]["x"], keypoints["left_shoulder"]["y"])
        r_sh = (keypoints["right_shoulder"]["x"], keypoints["right_shoulder"]["y"])

        # 1. Knee Angles & Valgus
        # Frontal knee angle: 180 is straight, deviation represents valgus/varus
        angle_l_leg = calculate_angle_2d(l_hip, l_knee, l_ankle)
        angle_r_leg = calculate_angle_2d(r_hip, r_knee, r_ankle)

        # Sagittal Knee Flexion (bending)
        metrics["knee_flexion_left"] = round(180.0 - angle_l_leg, 1)
        metrics["knee_flexion_right"] = round(180.0 - angle_r_leg, 1)

        # Knee Valgus: Frontal plane medial displacement
        # A person facing the camera: left knee moving rightward (towards midline) is medial collapse
        midline_x = (l_hip[0] + r_hip[0]) / 2.0
        valgus_l = max(0.0, round(abs(180.0 - angle_l_leg) * 0.75, 1))
        valgus_r = max(0.0, round(abs(180.0 - angle_r_leg) * 0.75, 1))

        # Check medial directional tendency
        if l_knee[0] > (l_hip[0] + l_ankle[0]) / 2.0:
            valgus_l = round(valgus_l * 1.3, 1) # Medial collapse confirmed
        if r_knee[0] < (r_hip[0] + r_ankle[0]) / 2.0:
            valgus_r = round(valgus_r * 1.3, 1)

        metrics["knee_valgus_left"] = min(valgus_l, 45.0)
        metrics["knee_valgus_right"] = min(valgus_r, 45.0)

        # 2. Trunk Lean (Lateral & Forward)
        sh_mid = ((l_sh[0] + r_sh[0]) / 2.0, (l_sh[1] + r_sh[1]) / 2.0)
        hip_mid = ((l_hip[0] + r_hip[0]) / 2.0, (l_hip[1] + r_hip[1]) / 2.0)
        
        dx = sh_mid[0] - hip_mid[0]
        dy = -(sh_mid[1] - hip_mid[1]) # Upwards is positive y
        trunk_angle_rad = math.atan2(abs(dx), max(dy, 1e-4))
        metrics["trunk_lateral_lean"] = round(math.degrees(trunk_angle_rad), 1)

        # Forward lean estimated from hip-shoulder vertical compression relative to height
        torso_len = math.hypot(dx, dy)
        expected_torso = 0.28 # Typical normalized height ratio
        if torso_len < expected_torso:
            lean_cos = min(1.0, max(0.2, torso_len / expected_torso))
            metrics["trunk_forward_lean"] = round(math.degrees(math.acos(lean_cos)), 1)
        else:
            metrics["trunk_forward_lean"] = 5.0

        # 3. Hip Stability / Pelvic Drop (Trendelenburg)
        hip_dy = abs(l_hip[1] - r_hip[1])
        hip_dx = max(abs(l_hip[0] - r_hip[0]), 1e-4)
        metrics["hip_stability_drop"] = round(math.degrees(math.atan2(hip_dy, hip_dx)), 1)

        # 4. Bilateral Asymmetry
        diff_valgus = abs(metrics["knee_valgus_left"] - metrics["knee_valgus_right"])
        diff_flex = abs(metrics["knee_flexion_left"] - metrics["knee_flexion_right"])
        asym = (diff_valgus * 2.0 + diff_flex * 0.5) / 2.5
        metrics["bilateral_asymmetry_pct"] = min(100.0, round(asym * 2.5, 1))

        # 5. Landing Force Proxy (g-force impact)
        # Stiffer knee (<35 deg flexion) under rapid movement multiplies ground reaction force
        avg_flex = (metrics["knee_flexion_left"] + metrics["knee_flexion_right"]) / 2.0
        if avg_flex < 30.0:
            metrics["landing_force_proxy_g"] = round(3.5 + (30.0 - avg_flex) * 0.08, 2)
        elif avg_flex < 50.0:
            metrics["landing_force_proxy_g"] = round(2.2 + (50.0 - avg_flex) * 0.06, 2)
        else:
            metrics["landing_force_proxy_g"] = 1.4

        # Risk Flags
        if metrics["knee_valgus_left"] > self.thresholds["knee_valgus"]["high_risk"]:
            metrics["flags"].append("Left Knee High Valgus Collapse (>15°)")
        if metrics["knee_valgus_right"] > self.thresholds["knee_valgus"]["high_risk"]:
            metrics["flags"].append("Right Knee High Valgus Collapse (>15°)")
        if metrics["trunk_lateral_lean"] > self.thresholds["trunk_lean_lateral"]["high_risk"]:
            metrics["flags"].append("Excessive Lateral Torso Sway")
        if metrics["hip_stability_drop"] > self.thresholds["pelvic_drop"]["high_risk"]:
            metrics["flags"].append("Severe Pelvic Drop (Glute Medius Instability)")

        return metrics

# Singleton
biomech_analyzer = BiomechanicsAnalyzer()
