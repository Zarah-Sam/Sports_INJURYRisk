# Sports Injury Risk Detection from Video

> **An AI-powered Sports Biomechanics and Injury Risk Intelligence Platform that analyzes athlete movement videos to identify biomechanical issues, detect abnormal movement patterns, assess injury risk factors, and predict potential injuries before they occur.**

Built with **FastAPI**, **YOLOv8-Pose (Ultralytics + PyTorch)**, **OpenCV (Cisco OpenH264)**, **Pydantic v2**, and a **Modern Glassmorphic HTML5 / Vanilla CSS / JavaScript Canvas UI**.

---

## 🏆 Completed Milestones Overview

### Milestone 1: Project Architecture, Data Modeling & Multi-Role Governance
- **System Architecture & Data Modeling:** Fully relational schema managed by a transactional JSON/memory state manager (`app_state.json`) with models for `User`, `Athlete`, `VideoRecord`, `BiomechanicalAnalysis`, `InjuryRiskAssessment`, and `Notification`.
- **User Authentication & Role-Based Access Control (RBAC):**
  - **5 Specialized Roles:** Athlete, Coach, Physiotherapist, Sports Scientist, and Administrator.
  - HMAC-SHA256 signed JWT tokens and instant 1-click role switcher in the navigation bar.
  - Pre-seeded demo accounts for instant evaluation across all roles.
- **Athlete Profile Management:**
  - Tracks Athlete ID, Sport Type, Position, Anthropometrics (Age, Height, Weight).
  - Longitudinal injury history tracking (injury type, occurrence year, clinical clearance status).
  - Training load metrics: Weekly session volume, Acute:Chronic Workload Ratio (ACWR), and acute fatigue indices.
  - Physical baseline assessment metrics.
- **Sports Biomechanics Datasets & Normative Baselines:**
  - Standard reference benchmarks integrated: **COCO 17-Keypoints**, **SportsPose**, and clinical normative kinematic distributions.
  - Clinical thresholds for knee valgus angles, landing knee flexion, trunk lean, bilateral asymmetry, and ACWR fatigue spikes.

---

### Milestone 2: Pose Estimation & Biomechanical Analysis
- **Pose Estimation Engine:**
  - Powered by **YOLOv8-Pose** extracting 17 anatomical landmarks (Nose, Shoulders, Elbows, Wrists, Hips, Knees, Ankles) with high-speed GPU/CPU inference.
  - Dynamic risk-reactive skeleton rendering with color-coded bones and joints:
    - 🟢 **Green:** Safe / optimal alignment
    - 🟡 **Amber:** Mild deviation
    - 🟠 **Orange:** Moderate risk threshold exceeded
    - 🔴 **Red:** Critical valgus collapse or high-impact shock
  - Frame-by-frame joint angle calculation for knees, hips, elbows, trunk lean, and pelvic obliquity.
- **Biomechanical Analysis Engine:**
  - **Dynamic Knee Valgus Angle (Frontal Plane Projection Angle / FPPA):** Measures medial knee collapse relative to the hip-ankle vector (primary biomarker for ACL tear prediction).
  - **Knee Flexion (Landing Mechanics):** Sagittal plane impact damping; detects high-force stiff landings (`< 35°`).
  - **Trunk Lean Dynamics:** Quantifies forward trunk lean (lumbar spine shear indicator) and lateral sway (core stabilizer deficit).
  - **Hip Stability & Pelvic Drop:** Trendelenburg sign detection for gluteus medius weakness.
  - **Bilateral Movement Asymmetry Index:** 
    $$\text{BAI} = \frac{|L - R|}{\max(L, R)} \times 100\%$$
  - **Ground Reaction Force (GRF) Proxy:** Kinetic impact force and shock acceleration estimation ($g$).
- **Synthetic Athletic Motion Generator:**
  - Built-in 1-click generator creating realistic biomechanical movements:
    - 💥 **Squat Knee Valgus:** Pronounced medial knee collapse.
    - 🦿 **High Jump Stiff Landing:** High-impact landing with low flexion (`< 35°`).
    - ⚡ **Sprint Cutting Drill:** Aggressive deceleration and lateral trunk tilt.
  - Encoded directly in universal **Cisco OpenH264 (`avc1`)** for seamless, zero-config HTML5 browser playback.
- **Real-Time Live Webcam Mode:**
  - Direct webcam stream processing via HTML5 Canvas with instant joint tracking and live valgus collapse HUD alerts.

---

### Milestone 3: Injury Risk Prediction & Corrective Recommendations
- **Weighted Scoring Engine (Strictly implements clinical blueprint formula):**
  $$\text{Injury Risk Score} = 0.35 \times \text{Biomechanical Deviations} + 0.20 \times \text{Historical Injury Factors} + 0.20 \times \text{Movement Asymmetry} + 0.15 \times \text{Training Load Indicators} + 0.10 \times \text{Fatigue Indicators}$$
  - **Low Risk:** 0 – 30
  - **Moderate Risk:** 31 – 60
  - **High Risk:** 61 – 80
  - **Critical Risk:** 81 – 100
- **Core Performance Indices:**
  - **Movement Quality Score** (0 – 100)
  - **Biomechanical Efficiency Score** (0 – 100)
  - **Overall Athlete Health Score** (0 – 100)
- **Injury Risk Prediction Engine (6 Clinical Categories):**
  - 🦵 **ACL Injury Risk:** Dynamic knee valgus (`> 14°`), low landing flexion, shear deceleration, past ACL reconstruction.
  - 🏃 **Hamstring Injury Risk:** Overstriding deceleration, anterior pelvic tilt, high eccentric sprinting load.
  - 👟 **Ankle Sprain Risk:** Lateral trunk sway, subtalar landing instability, ground reaction force spikes (`> 3.0g`).
  - 💪 **Shoulder Dyskinesis Risk:** Overhead arm acceleration and scapulothoracic torque leakage.
  - 🛡️ **Lower Back / Lumbar Strain Risk:** Excessive forward trunk lean (`> 25°`) and asymmetric lumbar loading.
  - ⏳ **Overuse Injury Risk:** Acute:Chronic Workload Ratio in danger zone (`ACWR > 1.45`) plus kinematic fatigue drift.
- **Movement Anomaly & Fatigue Detection Engine:**
  - Frame-by-frame anomaly detection across kinematic thresholds.
  - Fatigue-related movement monitoring measuring kinematic decay across movement cycles.
- **Corrective Recommendation Engine:**
  - Prescribes targeted clinical exercises with sets, reps, frequency, and coaching cues:
    - *Banded Monster Walks & Clamshells* for knee valgus / gluteus medius weakness.
    - *Nordic Hamstring Curls & Romanian Deadlifts* for hamstring strain mitigation.
    - *Single-Leg Stick Landings* for stiff landing mechanics.
    - *McGill Big 3 & Pallof Press* for trunk lean and core stabilization.
- **5 Role-Specific Intelligence Dashboards:**
  - **Athlete Dashboard:** Personal risk dial, readiness index, and daily corrective exercise checklist.
  - **Coach Dashboard:** Squad roster availability %, team injury risk heatmap, and load restrictions.
  - **Physiotherapist Dashboard:** Clinical rehabilitation registry, ROM recovery curves, and bilateral deficit tracking.
  - **Sports Scientist Dashboard:** Kinematic waveform time-series, population benchmark comparison, and raw data analytics.
  - **Administrator Dashboard:** System health, YOLOv8 inference latency (ms), model weights status, and audit logs.
- **Clinical Reporting & Data Export:**
  - High-resolution, print-ready HTML/PDF clinical biomechanics assessment reports (`/api/reports/{id}/html`).
  - Full telemetry CSV dataset export (`/api/reports/export-csv`).

---

## 🚀 Quick Start Guide

### 1. Launch the Application (One-Click)
In the project directory, run:
```powershell
python run.py
```

### 2. Access the Platform
- **Web Application UI:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive OpenAPI Documentation (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Health Check:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 👥 Seed User Accounts

All accounts are pre-configured with instant 1-click preview via the **Role Switcher** in the top navigation bar:

| Role | Email | Name | Focus Area |
| :--- | :--- | :--- | :--- |
| **Athlete** | `marcus.vance@eliteathletics.org` | Marcus Vance | Personal Risk Score, Readiness, Today's Corrective Workout |
| **Coach** | `coach.miller@fcpremier.com` | Coach Dave Miller | Squad Availability %, Team Heatmap, Minutes Restrictions |
| **Physiotherapist** | `dr.patel@sportsrehab.clinic` | Dr. Priya Patel (PT, DPT) | Clinical Rehab Registry, Joint ROM, Bilateral Symmetry |
| **Sports Scientist** | `aris.thorne@biomech-institute.edu` | Dr. Aris Thorne | Kinematic Waveforms, SportsPose Comparison, CSV Exports |
| **Administrator** | `admin@biomech-intel.com` | Systems Administrator | Platform Health, Inference Latency (ms), Model Weights |

---

## 🧪 System Verification & Architecture Tests

To verify backend modules, mathematical scoring logic, and model inference:

```powershell
# Verify Python environment & ML stack
python -c "import cv2, ultralytics, torch, fastapi; print('Stack operational')"

# Test synthetic motion generation & H.264 video rendering
python -c "from backend.services.synthetic_motion import generate_demo_video; generate_demo_video('valgus_squat'); print('Video encoder operational')"

# Run full API assessment pipeline test
python -c "from backend.services.video_processor import video_processor; from pathlib import Path; res = video_processor.process_video_file(Path('data/uploads/demo_valgus_squat.mp4')); print('Assessment pipeline passed:', res['id'])"
```
