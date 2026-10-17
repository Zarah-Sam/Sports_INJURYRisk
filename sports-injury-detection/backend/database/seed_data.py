"""
Default Seed Data for Athletes, Users, Assessments, and Notifications
"""
import datetime

DEFAULT_USERS = [
    {
        "id": "USR-001",
        "email": "marcus.vance@eliteathletics.org",
        "full_name": "Marcus Vance",
        "role": "athlete",
        "athlete_id": "ATH-001",
        "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"
    },
    {
        "id": "USR-002",
        "email": "coach.miller@fcpremier.com",
        "full_name": "Coach Dave Miller",
        "role": "coach",
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80"
    },
    {
        "id": "USR-003",
        "email": "dr.patel@sportsrehab.clinic",
        "full_name": "Dr. Priya Patel (PT, DPT)",
        "role": "physiotherapist",
        "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80"
    },
    {
        "id": "USR-004",
        "email": "aris.thorne@biomech-institute.edu",
        "full_name": "Dr. Aris Thorne",
        "role": "sports_scientist",
        "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80"
    },
    {
        "id": "USR-005",
        "email": "admin@biomech-intel.com",
        "full_name": "Systems Administrator",
        "role": "administrator",
        "avatar_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80"
    }
]

DEFAULT_ATHLETES = [
    {
        "athlete_id": "ATH-001",
        "full_name": "Marcus Vance",
        "sport_type": "Soccer",
        "position": "Forward / Striker",
        "age": 23,
        "height_cm": 185.0,
        "weight_kg": 78.5,
        "injury_history": [
            {"injury": "Left ACL Reconstruction", "year": 2024, "status": "Cleared, Guarded"},
            {"injury": "Medial Collateral Sprain", "year": 2023, "status": "Resolved"}
        ],
        "training_load": {
            "weekly_sessions": 6,
            "weekly_rpe_volume": 4200,
            "acwr": 1.42, # High Acute:Chronic Workload
            "fatigue_index": 72
        },
        "latest_risk_score": 68.5,
        "risk_category": "High Risk",
        "movement_quality_score": 64.0,
        "last_assessment_date": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
    },
    {
        "athlete_id": "ATH-002",
        "full_name": "Elena Rostova",
        "sport_type": "Track & Field",
        "position": "100m / 200m Sprinter",
        "age": 21,
        "height_cm": 172.0,
        "weight_kg": 62.0,
        "injury_history": [
            {"injury": "Right Biceps Femoris (Hamstring) Strain Gr 2", "year": 2025, "status": "Active Rehab"}
        ],
        "training_load": {
            "weekly_sessions": 7,
            "weekly_rpe_volume": 3800,
            "acwr": 1.28,
            "fatigue_index": 58
        },
        "latest_risk_score": 54.0,
        "risk_category": "Moderate Risk",
        "movement_quality_score": 78.0,
        "last_assessment_date": (datetime.datetime.now() - datetime.timedelta(days=3)).isoformat()
    },
    {
        "athlete_id": "ATH-003",
        "full_name": "David Kim",
        "sport_type": "Basketball",
        "position": "Point Guard",
        "age": 25,
        "height_cm": 191.0,
        "weight_kg": 86.0,
        "injury_history": [
            {"injury": "Lateral Inversion Ankle Sprain (Grade 2)", "year": 2025, "status": "Chronic Instability"}
        ],
        "training_load": {
            "weekly_sessions": 5,
            "weekly_rpe_volume": 3600,
            "acwr": 1.15,
            "fatigue_index": 45
        },
        "latest_risk_score": 42.0,
        "risk_category": "Moderate Risk",
        "movement_quality_score": 81.0,
        "last_assessment_date": (datetime.datetime.now() - datetime.timedelta(days=5)).isoformat()
    },
    {
        "athlete_id": "ATH-004",
        "full_name": "Maya Lin",
        "sport_type": "Volleyball",
        "position": "Outside Hitter",
        "age": 22,
        "height_cm": 183.0,
        "weight_kg": 70.0,
        "injury_history": [
            {"injury": "Patellar Tendinopathy (Jumper's Knee)", "year": 2024, "status": "Managed"}
        ],
        "training_load": {
            "weekly_sessions": 5,
            "weekly_rpe_volume": 3100,
            "acwr": 0.98,
            "fatigue_index": 30
        },
        "latest_risk_score": 24.5,
        "risk_category": "Low Risk",
        "movement_quality_score": 91.0,
        "last_assessment_date": (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat()
    },
    {
        "athlete_id": "ATH-005",
        "full_name": "Sarah Jenkins",
        "sport_type": "CrossFit / Olympic Lifting",
        "position": "Competitive Open",
        "age": 28,
        "height_cm": 168.0,
        "weight_kg": 67.5,
        "injury_history": [
            {"injury": "L5-S1 Lumbar Disc Bulge", "year": 2023, "status": "Asymptomatic"}
        ],
        "training_load": {
            "weekly_sessions": 6,
            "weekly_rpe_volume": 4900,
            "acwr": 1.55, # Overtraining hazard
            "fatigue_index": 82
        },
        "latest_risk_score": 84.0,
        "risk_category": "Critical Risk",
        "movement_quality_score": 52.0,
        "last_assessment_date": (datetime.datetime.now() - datetime.timedelta(hours=6)).isoformat()
    }
]

DEFAULT_ASSESSMENTS = [
    {
        "id": "ASM-INIT-001",
        "athlete_id": "ATH-001",
        "athlete_name": "Marcus Vance",
        "activity_type": "Jump Landing & Deceleration",
        "created_at": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
        "overall_risk_score": 68.5,
        "risk_category": "High Risk",
        "movement_quality_score": 64.0,
        "biomechanical_metrics": {
            "knee_valgus_left": 16.8,      # Critical left knee valgus collapse
            "knee_valgus_right": 7.2,
            "knee_flexion_left": 31.4,     # Stiff landing <35 deg
            "knee_flexion_right": 46.5,
            "trunk_forward_lean": 24.2,
            "trunk_lateral_lean": 12.1,
            "hip_stability_drop": 8.4,
            "bilateral_asymmetry_pct": 21.5,
            "landing_force_proxy_g": 3.8
        },
        "weighted_breakdown": {
            "biomechanical_deviations": 74.0,  # 35% weight -> 25.9
            "historical_injury_factors": 85.0, # 20% weight -> 17.0
            "movement_asymmetry": 68.0,        # 20% weight -> 13.6
            "training_load_indicators": 55.0,  # 15% weight -> 8.25
            "fatigue_indicators": 37.5         # 10% weight -> 3.75
        },
        "detected_injuries": [
            {"category": "ACL Injury Risk", "level": "High", "probability": 84, "key_factors": "Severe left knee valgus collapse (16.8°) + Stiff knee impact (<32° flexion)"},
            {"category": "Hamstring Injury Risk", "level": "Low", "probability": 28, "key_factors": "Submaximal sprint angle, minor pelvic anterior tilt"},
            {"category": "Ankle Sprain Risk", "level": "Moderate", "probability": 48, "key_factors": "Compensatory left foot pronation on ground contact"},
            {"category": "Lower Back Injury Risk", "level": "Low", "probability": 22, "key_factors": "Trunk forward lean within safe margins (<25°)"},
            {"category": "Overuse Injury Risk", "level": "Moderate", "probability": 56, "key_factors": "Acute:Chronic Workload Ratio (1.42) approaching dangerous zone"}
        ],
        "recommendations": {
            "exercises": [
                {"name": "Banded Squat Hold with External Rotation", "sets": "4 sets x 12 reps", "focus": "Activates gluteus medius to eliminate medial knee collapse"},
                {"name": "Single-Leg Drop Landing to Soft Box", "sets": "3 sets x 6 reps/leg", "focus": "Forces knee flexion shock absorption >45°"},
                {"name": "Side-Lying Clamshells with Resistance Band", "sets": "3 sets x 15 reps", "focus": "Hip abductor endurance"}
            ],
            "mobility": ["90/90 Hip Rotations (3 mins)", "Ankle Dorsiflexion Wall Mobilization (2 mins/side)"],
            "training_modification": "Cap maximal cutting & deceleration drills at 65% velocity until valgus angle stabilizes below 10°.",
            "recovery_plan": "Implement 15-minute contrast water therapy post training sessions."
        }
    }
]

DEFAULT_NOTIFICATIONS = [
    {
        "id": "NOTIF-01",
        "athlete_id": "ATH-001",
        "title": "Severe Knee Valgus Collapse Detected",
        "severity": "high",
        "message": "Marcus Vance displayed 16.8° medial knee deviation during jump deceleration. ACL protective threshold exceeded.",
        "timestamp": (datetime.datetime.now() - datetime.timedelta(hours=2)).isoformat(),
        "read": False
    },
    {
        "id": "NOTIF-02",
        "athlete_id": "ATH-005",
        "title": "Critical Acute Workload Spike (ACWR 1.55)",
        "severity": "critical",
        "message": "Sarah Jenkins has entered the high injury danger zone due to back-to-back high intensity lifting sessions.",
        "timestamp": (datetime.datetime.now() - datetime.timedelta(hours=5)).isoformat(),
        "read": False
    },
    {
        "id": "NOTIF-03",
        "athlete_id": "ATH-002",
        "title": "Hamstring Rehabilitation Progress Notice",
        "severity": "info",
        "message": "Elena Rostova completed weekly kinematic assessment: Bilateral sprint asymmetry reduced by 6.4%.",
        "timestamp": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
        "read": True
    }
]
