"""
Injury Risk Prediction Engine
Predicts specific sport injury probabilities across 6 key clinical categories:
1. ACL Injury Risk
2. Hamstring Injury Risk
3. Ankle Sprain Risk
4. Shoulder Injury Risk
5. Lower Back Injury Risk
6. Overuse Injury Risk
"""
from typing import Dict, Any, List

class InjuryPredictor:
    def __init__(self):
        pass

    def predict_injuries(
        self,
        biomech_summary: Dict[str, float],
        anomaly_summary: Dict[str, Any],
        athlete_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        results = []

        max_valgus = max(biomech_summary.get("knee_valgus_left", 0), biomech_summary.get("knee_valgus_right", 0))
        min_flex = min(biomech_summary.get("knee_flexion_left", 60), biomech_summary.get("knee_flexion_right", 60))
        trunk_forward = biomech_summary.get("trunk_forward_lean", 15)
        trunk_lateral = biomech_summary.get("trunk_lateral_lean", 5)
        pelvic_drop = biomech_summary.get("hip_stability_drop", 4)
        asym = biomech_summary.get("bilateral_asymmetry_pct", 10)
        landing_g = biomech_summary.get("landing_force_proxy_g", 1.5)
        
        hist_text = " ".join([str(x) for x in athlete_profile.get("injury_history", [])]).lower()
        acwr = athlete_profile.get("training_load", {}).get("acwr", 1.1)

        # 1. ACL Injury Risk (Knee Valgus + Stiff Knee Landing + Cutting)
        acl_score = 10.0
        acl_factors = []
        if max_valgus > 14.0:
            acl_score += 45.0
            acl_factors.append(f"Severe knee abduction (valgus peak {max_valgus}°)")
        elif max_valgus > 9.0:
            acl_score += 25.0
            acl_factors.append(f"Moderate medial knee collapse ({max_valgus}°)")

        if min_flex < 35.0:
            acl_score += 25.0
            acl_factors.append(f"Stiff-legged ground impact (flexion {min_flex}° raises ACL shear stress)")
        
        if "acl" in hist_text:
            acl_score += 20.0
            acl_factors.append("Prior ACL reconstruction (increased ipsilateral/contralateral risk)")

        results.append(self._format_risk("ACL Injury Risk", min(98, acl_score), acl_factors or ["Sufficient sagittal knee flexion and frontal stability"]))

        # 2. Hamstring Injury Risk (Overstriding, Pelvic Anterior Tilt, Sprint Asymmetry)
        ham_score = 12.0
        ham_factors = []
        if asym > 18.0:
            ham_score += 35.0
            ham_factors.append(f"Elevated bilateral limb asymmetry ({asym}%) causes uneven eccentric loading")
        if pelvic_drop > 8.0:
            ham_score += 25.0
            ham_factors.append(f"Excessive pelvic tilt/drop ({pelvic_drop}°) pre-stretches proximal hamstring")
        if "hamstring" in hist_text:
            ham_score += 25.0
            ham_factors.append("Prior hamstring strain history")

        results.append(self._format_risk("Hamstring Injury Risk", min(95, ham_score), ham_factors or ["Balanced bilateral limb extension and pelvic control"]))

        # 3. Ankle Sprain Risk (Landing Instability, Lateral Sway, Bilateral Deficit)
        ankle_score = 15.0
        ankle_factors = []
        if trunk_lateral > 12.0:
            ankle_score += 30.0
            ankle_factors.append(f"Excessive lateral trunk sway ({trunk_lateral}°) shifts ground reaction vector outward")
        if landing_g > 3.0:
            ankle_score += 25.0
            ankle_factors.append(f"High ground reaction impact ({landing_g}g)")
        if "ankle" in hist_text:
            ankle_score += 25.0
            ankle_factors.append("Chronic ankle joint laxity / recurrent sprains")

        results.append(self._format_risk("Ankle Sprain Risk", min(92, ankle_score), ankle_factors or ["Stable center of mass alignment over ankle base"]))

        # 4. Shoulder Injury Risk (Throwing/Upper Body Deceleration)
        sh_score = 15.0
        sh_factors = []
        sport = str(athlete_profile.get("sport_type", "")).lower()
        if "tennis" in sport or "volleyball" in sport or "baseball" in sport:
            sh_score += 20.0
            sh_factors.append("High repetitive overhead arm acceleration demand")
        if "shoulder" in hist_text:
            sh_score += 30.0
            sh_factors.append("Previous rotator cuff / labrum pathology")

        results.append(self._format_risk("Shoulder Injury Risk", min(85, sh_score), sh_factors or ["Normal scapulothoracic rhythm observed"]))

        # 5. Lower Back Injury Risk (Excessive Forward Lumbar Flexion / Shear)
        back_score = 10.0
        back_factors = []
        if trunk_forward > 38.0:
            back_score += 45.0
            back_factors.append(f"Excessive trunk forward lean ({trunk_forward}°) multiplies lumbar spine moment arm")
        elif trunk_forward > 28.0:
            back_score += 20.0
            back_factors.append(f"Moderate trunk flexion ({trunk_forward}°)")

        if "back" in hist_text or "lumbar" in hist_text or "disc" in hist_text:
            back_score += 25.0
            back_factors.append("Pre-existing lumbar disc/spine history")

        results.append(self._format_risk("Lower Back Injury Risk", min(94, back_score), back_factors or ["Neutral spine maintained within safe biomechanical parameters"]))

        # 6. Overuse Injury Risk (ACWR Spikes, Fatigue Degradation)
        overuse_score = 10.0
        overuse_factors = []
        if acwr > 1.5:
            overuse_score += 50.0
            overuse_factors.append(f"Acute:Chronic Workload Ratio in danger spike zone ({acwr} > 1.5)")
        elif acwr > 1.3:
            overuse_score += 25.0
            overuse_factors.append(f"Elevated workload buildup ({acwr})")

        if anomaly_summary.get("fatigue_degradation_detected"):
            overuse_score += 25.0
            overuse_factors.append("Motor control breakdown observed during fatigue phase of movement")

        results.append(self._format_risk("Overuse Injury Risk", min(96, overuse_score), overuse_factors or ["Well-regulated training volume and minimal fatigue kinematic drift"]))

        # Sort with highest risk first
        results.sort(key=lambda x: x["probability"], reverse=True)
        return results

    def _format_risk(self, category: str, prob: float, factors: List[str]) -> Dict[str, Any]:
        prob = round(prob, 1)
        if prob >= 70:
            level = "High"
            color = "#ef4444"
        elif prob >= 40:
            level = "Moderate"
            color = "#f59e0b"
        else:
            level = "Low"
            color = "#10b981"

        return {
            "category": category,
            "level": level,
            "probability": prob,
            "color": color,
            "key_factors": "; ".join(factors)
        }

# Singleton
injury_predictor = InjuryPredictor()
