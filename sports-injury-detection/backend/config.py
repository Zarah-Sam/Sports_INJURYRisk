"""
Sports Injury Risk Detection System - Configuration
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
PROCESSED_DIR = DATA_DIR / "processed"
REPORT_DIR = DATA_DIR / "reports"
STATIC_DIR = BASE_DIR / "frontend" / "static"
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
MODEL_DIR = BASE_DIR / "backend" / "engine"

# Ensure runtime directories exist
for p in [UPLOAD_DIR, PROCESSED_DIR, REPORT_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# Security and JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "sports-injury-ai-super-secret-key-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# Biomechanical and Scoring Weights (As defined in System Specifications)
SCORING_WEIGHTS = {
    "biomechanical_deviations": 0.35,
    "historical_injury_factors": 0.20,
    "movement_asymmetry": 0.20,
    "training_load_indicators": 0.15,
    "fatigue_indicators": 0.10,
}

# Biomechanical Normal & Risk Thresholds (degrees)
THRESHOLDS = {
    "knee_valgus": {
        "safe_max": 8.0,        # <8 deg frontal deviation is normal
        "caution_max": 14.0,    # 8-14 deg mild valgus
        "high_risk": 15.0       # >15 deg severe valgus collapse (ACL trigger)
    },
    "knee_flexion_landing": {
        "stiff_landing": 35.0,  # <35 deg flexion on impact = high ground reaction force
        "optimal_min": 45.0,    # 45-90 deg optimal shock absorption
    },
    "trunk_lean_forward": {
        "normal_max": 30.0,
        "high_risk": 45.0       # >45 deg excessive shear on lumbar spine
    },
    "trunk_lean_lateral": {
        "normal_max": 8.0,
        "high_risk": 15.0       # >15 deg lateral torso sway indicates core instability
    },
    "pelvic_drop": {
        "normal_max": 5.0,
        "high_risk": 10.0       # >10 deg Trendelenburg sign / glute medius weakness
    },
    "bilateral_asymmetry": {
        "safe_max": 10.0,       # <10% asymmetry
        "high_risk": 15.0       # >15% bilateral deficit increases re-injury risk
    }
}
