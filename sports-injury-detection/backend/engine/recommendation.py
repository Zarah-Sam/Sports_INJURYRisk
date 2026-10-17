"""
Corrective Recommendation Engine
Generates tailored corrective exercise regimens, mobility protocols,
strengthening prescriptions, and training load adjustments based on biomechanical deficits.
"""
from typing import Dict, Any, List

class RecommendationEngine:
    def __init__(self):
        pass

    def generate_recommendations(
        self,
        injury_predictions: List[Dict[str, Any]],
        biomech_summary: Dict[str, float],
        athlete_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        exercises = []
        mobility = []
        strengthening = []
        training_modifications = []
        recovery_plan = []

        top_risks = [inj for inj in injury_predictions if inj["level"] in ["High", "Moderate"]]
        
        # 1. Correctives for ACL / Knee Valgus
        has_acl_risk = any(inj["category"] == "ACL Injury Risk" and inj["level"] in ["High", "Moderate"] for inj in top_risks)
        if has_acl_risk or biomech_summary.get("knee_valgus_left", 0) > 10.0 or biomech_summary.get("knee_valgus_right", 0) > 10.0:
            exercises.append({
                "name": "Banded Lateral Monster Walks with Deep Squat Hold",
                "target": "Gluteus Medius & Hip External Rotators",
                "dose": "4 sets x 15 steps per direction",
                "cues": "Maintain continuous band tension; keep knees pushed outward over 2nd toe; avoid knee caving."
            })
            exercises.append({
                "name": "Single-Leg Drop Jump to Soft Stick Landing",
                "target": "Sagittal Deceleration & Knee Flexion Shock Absorption",
                "dose": "3 sets x 6 reps per leg (30cm box)",
                "cues": "Quiet landing like a ninja; sink into 60° knee bend; ensure knee tracks directly above the foot."
            })
            strengthening.append("Heavy Barbell Romanian Deadlifts (RDL) 4x8 @ 75% 1RM for posterior chain stiffness")
            mobility.append("Ankle Dorsiflexion Knee-to-Wall Mobilizations (2 mins/side) to eliminate compensatory foot pronation")
            training_modifications.append("Reduce high-velocity reactive cutting drills by 40% until valgus angle < 8°.")

        # 2. Correctives for Hamstring Strain Risk
        has_ham_risk = any(inj["category"] == "Hamstring Injury Risk" and inj["level"] in ["High", "Moderate"] for inj in top_risks)
        if has_ham_risk:
            exercises.append({
                "name": "Nordic Hamstring Curls (Assisted Eccentric Phase)",
                "target": "Biceps Femoris Eccentric Strength & Fascicle Length",
                "dose": "3 sets x 5 reps (4-second lowering)",
                "cues": "Maintain neutral pelvis; fight the descent as long as possible before catching yourself."
            })
            exercises.append({
                "name": "Single-Leg Slider Hamstring Curls",
                "target": "Closed-Chain Hamstring Activation",
                "dose": "3 sets x 10 reps per leg",
                "cues": "Keep hips elevated in bridge position while curling the heel under the glute."
            })
            mobility.append("Active Straight Leg Raise PNF Stretching with Band (3 sets of 10-second contract-relax)")
            training_modifications.append("Restrict maximal sprint acceleration to 85% velocity during fatigue blocks.")

        # 3. Correctives for Ankle Instability / Inversion Risk
        has_ankle_risk = any(inj["category"] == "Ankle Sprain Risk" and inj["level"] in ["High", "Moderate"] for inj in top_risks)
        if has_ankle_risk:
            exercises.append({
                "name": "Single-Leg Balance on Foam Pad with Eyes Closed",
                "target": "Subtalar Proprioception & Peroneal Reflex Reaction",
                "dose": "4 sets x 45 seconds per side",
                "cues": "Engage the foot tripod (heel, 1st metatarsal, 5th metatarsal); maintain quiet ankle."
            })
            strengthening.append("Eccentric Tibialis Anterior & Peroneus Longus Calf Drops from Step 3x15 reps")
            mobility.append("Subtalar Joint Banded Distraction (90 seconds per side)")

        # 4. Correctives for Lower Back / Excessive Trunk Lean
        has_back_risk = any(inj["category"] == "Lower Back Injury Risk" and inj["level"] in ["High", "Moderate"] for inj in top_risks)
        if has_back_risk or biomech_summary.get("trunk_forward_lean", 0) > 30.0:
            exercises.append({
                "name": "McGill Big 3 (Bird-Dog, Side Bridge, Modified Curl-Up)",
                "target": "Lumbar Anti-Extension & Anti-Rotation Torso Stiffness",
                "dose": "Descending pyramid: 5-4-3-2 reps (8-sec hold)",
                "cues": "Lock ribcage to pelvis; breathe through the diaphragm while maintaining abdominal brace."
            })
            exercises.append({
                "name": "Half-Kneeling Cable Pallof Press",
                "target": "Rotary Core Stability & Pelvic Symmetry",
                "dose": "3 sets x 12 reps per side",
                "cues": "Do not let the cable pull your torso toward the anchor; stay perfectly square."
            })
            strengthening.append("Neutral Spine Safety Bar Box Squats to reinforce upright torso posture")
            training_modifications.append("Cease Olympic lifts and heavy deadlifts at fatigue thresholds; substitute with belt squats.")

        # 5. Overuse / Recovery Planning
        acwr = athlete_profile.get("training_load", {}).get("acwr", 1.1)
        if acwr > 1.4:
            training_modifications.append(f"CRITICAL: ACWR is {acwr}. Execute an immediate 30% volume deload for the next 72 hours.")
            recovery_plan.append("Target 8.5 to 9.0 hours of sleep with sleep hygiene monitoring.")
            recovery_plan.append("20-minute Contrast Hydrotherapy protocol (3 min cold @ 10°C / 1 min warm @ 38°C).")
            recovery_plan.append("Electrolyte rehydration and anti-inflammatory nutrition protocol (Omega-3 + Tart Cherry).")
        else:
            recovery_plan.append("Standard 15-minute post-practice cool-down with soft tissue foam rolling.")
            recovery_plan.append("Active recovery flush ride (20 mins @ 60% HRmax).")

        # Fallback default if athlete is low risk
        if not exercises:
            exercises.append({
                "name": "Isometric Single-Leg Glute Bridges",
                "target": "Hip Extension Stability Maintenance",
                "dose": "3 sets x 30 second hold",
                "cues": "Squeeze glute without arching lumbar spine."
            })
            mobility.append("World's Greatest Stretch Routine (5 reps per side)")
            training_modifications.append("Athlete cleared for 100% full competitive workload.")

        return {
            "exercises": exercises,
            "strengthening": strengthening,
            "mobility": mobility,
            "training_modification": " | ".join(training_modifications),
            "recovery_plan": recovery_plan
        }

# Singleton
recommendation_engine = RecommendationEngine()
