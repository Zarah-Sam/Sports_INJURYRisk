"""
Reports & Export System
Generates professional clinical biomechanical reports, printable PDF-ready HTML,
and CSV export data for sports scientists and medical teams.
"""
import io
import csv
from typing import Dict, Any, Optional
from backend.database.db import db

class ReportGenerator:
    def __init__(self):
        pass

    def generate_html_report(self, assessment_id: str) -> Optional[str]:
        """Generates a high-resolution, print-ready HTML assessment report."""
        record = db.get_assessment(assessment_id)
        if not record:
            return None

        ath = db.get_athlete(record.get("athlete_id", "")) or {}
        bio = record.get("biomechanical_metrics", {})
        breakdown = record.get("weighted_breakdown", {})
        injuries = record.get("detected_injuries", [])
        recs = record.get("recommendations", {})

        injuries_rows = "".join([
            f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: 600;">{inj.get('category')}</td>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">
                    <span style="background: {inj.get('color', '#64748b')}22; color: {inj.get('color', '#64748b')}; padding: 4px 10px; border-radius: 999px; font-weight: 700; font-size: 12px;">
                        {inj.get('level')} ({inj.get('probability')}%)
                    </span>
                </td>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; color: #475569;">{inj.get('key_factors')}</td>
            </tr>
            """
            for inj in injuries
        ])

        exercises_list = "".join([
            f"""
            <li style="margin-bottom: 8px;">
                <strong>{ex.get('name')}</strong> — <span style="color: #6366f1;">{ex.get('dose')}</span><br>
                <small style="color: #64748b;">Target: {ex.get('target')} | Cue: {ex.get('cues')}</small>
            </li>
            """
            for ex in recs.get("exercises", [])
        ])

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Clinical Biomechanical Assessment - {record.get('id')}</title>
    <style>
        @page {{ size: A4; margin: 20mm; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.5; margin: 0; padding: 24px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0f172a; padding-bottom: 16px; margin-bottom: 24px; }}
        .logo-title h1 {{ margin: 0; font-size: 24px; color: #0f172a; letter-spacing: -0.5px; }}
        .logo-title p {{ margin: 4px 0 0; color: #64748b; font-size: 13px; }}
        .badge {{ background: {record.get('category_color', '#f59e0b')}; color: white; padding: 6px 16px; border-radius: 6px; font-weight: 700; font-size: 14px; text-transform: uppercase; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
        .card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; }}
        .card h3 {{ margin: 0 0 12px; font-size: 15px; color: #334155; text-transform: uppercase; letter-spacing: 0.5px; }}
        .metric-row {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px dashed #cbd5e1; font-size: 13px; }}
        .metric-row:last-child {{ border-bottom: none; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; margin-top: 12px; }}
        th {{ background: #f1f5f9; padding: 10px; font-size: 12px; text-transform: uppercase; color: #475569; }}
        .score-box {{ text-align: center; padding: 16px; background: #0f172a; color: white; border-radius: 8px; }}
        .score-val {{ font-size: 44px; font-weight: 800; color: {record.get('category_color', '#38bdf8')}; margin: 4px 0; }}
        @media print {{
            body {{ padding: 0; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="no-print" style="margin-bottom: 20px; text-align: right;">
        <button onclick="window.print()" style="background: #2563eb; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer;">
            🖨️ Print / Save as PDF
        </button>
    </div>

    <div class="header">
        <div class="logo-title">
            <h1>SPORTS INJURY RISK DETECTION PLATFORM</h1>
            <p>Biomechanical Motion Assessment & Clinical Risk Report | Ref: {record.get('id')}</p>
        </div>
        <div class="badge">{record.get('risk_category')}</div>
    </div>

    <div class="grid">
        <div class="card">
            <h3>Athlete Profile</h3>
            <div class="metric-row"><span>Athlete Name:</span> <strong>{record.get('athlete_name')}</strong></div>
            <div class="metric-row"><span>Athlete ID:</span> <span>{record.get('athlete_id')}</span></div>
            <div class="metric-row"><span>Sport / Position:</span> <span>{ath.get('sport_type', 'N/A')} ({ath.get('position', 'N/A')})</span></div>
            <div class="metric-row"><span>Assessment Date:</span> <span>{record.get('created_at', '')[:10]}</span></div>
            <div class="metric-row"><span>Activity Evaluated:</span> <span>{record.get('activity_type')}</span></div>
            <div class="metric-row"><span>Acute:Chronic Workload (ACWR):</span> <span>{ath.get('training_load', {}).get('acwr', '1.20')}</span></div>
        </div>

        <div class="score-box">
            <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8;">Composite Injury Risk Score</div>
            <div class="score-val">{record.get('overall_risk_score')} <span style="font-size: 18px; color: #94a3b8;">/ 100</span></div>
            <div style="font-size: 14px; font-weight: 600;">Movement Quality: {record.get('movement_quality_score')}% | Health Index: {record.get('athlete_health_score')}%</div>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <h3>Biomechanical Telemetry</h3>
            <div class="metric-row"><span>Left Knee Valgus (Frontal):</span> <strong>{bio.get('knee_valgus_left')}°</strong></div>
            <div class="metric-row"><span>Right Knee Valgus:</span> <span>{bio.get('knee_valgus_right')}°</span></div>
            <div class="metric-row"><span>Peak Landing Knee Flexion:</span> <span>L: {bio.get('knee_flexion_left')}° | R: {bio.get('knee_flexion_right')}°</span></div>
            <div class="metric-row"><span>Trunk Lateral Sway:</span> <span>{bio.get('trunk_lateral_lean')}°</span></div>
            <div class="metric-row"><span>Trunk Forward Lean:</span> <span>{bio.get('trunk_forward_lean')}°</span></div>
            <div class="metric-row"><span>Pelvic Drop / Unleveling:</span> <span>{bio.get('hip_stability_drop')}°</span></div>
            <div class="metric-row"><span>Bilateral Limb Asymmetry:</span> <strong>{bio.get('bilateral_asymmetry_pct')}%</strong></div>
            <div class="metric-row"><span>Landing Force Impact Proxy:</span> <span>{bio.get('landing_force_proxy_g')} g</span></div>
        </div>

        <div class="card">
            <h3>Weighted Risk Model Breakdown</h3>
            <div class="metric-row"><span>Biomechanical Deviations (35%):</span> <strong>{breakdown.get('biomechanical_deviations')}/100</strong></div>
            <div class="metric-row"><span>Historical Injury Factors (20%):</span> <span>{breakdown.get('historical_injury_factors')}/100</span></div>
            <div class="metric-row"><span>Movement Asymmetry (20%):</span> <span>{breakdown.get('movement_asymmetry')}/100</span></div>
            <div class="metric-row"><span>Training Load Indicators (15%):</span> <span>{breakdown.get('training_load_indicators')}/100</span></div>
            <div class="metric-row"><span>Fatigue Indicators (10%):</span> <span>{breakdown.get('fatigue_indicators')}/100</span></div>
        </div>
    </div>

    <div class="card" style="margin-bottom: 24px;">
        <h3>Categorical Injury Risk Predictions</h3>
        <table>
            <thead>
                <tr>
                    <th>Injury Category</th>
                    <th>Risk Level</th>
                    <th>Identified Clinical Indicators</th>
                </tr>
            </thead>
            <tbody>
                {injuries_rows}
            </tbody>
        </table>
    </div>

    <div class="card">
        <h3>Prescribed Corrective Intervention Plan</h3>
        <p><strong>Training Modification:</strong> {recs.get('training_modification', 'Normal training')}</p>
        <p><strong>Targeted Strengthening Exercises:</strong></p>
        <ul>
            {exercises_list}
        </ul>
        <p><strong>Mobility Protocol:</strong> {", ".join(recs.get('mobility', []))}</p>
        <p><strong>Recovery Protocol:</strong> {", ".join(recs.get('recovery_plan', []))}</p>
    </div>

    <div style="margin-top: 30px; font-size: 11px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 12px; text-align: center;">
        Automated Biomechanical Intelligence Platform | Compliant with Clinical Sports Biomechanics Protocol | Confidential Medical Document
    </div>
</body>
</html>"""
        return html

    def generate_csv_export(self, athlete_id: Optional[str] = None) -> str:
        """Exports assessments to CSV format for sports scientist research."""
        assessments = db.get_assessments(athlete_id)
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow([
            "Assessment_ID", "Athlete_ID", "Athlete_Name", "Activity", "Date",
            "Overall_Risk_Score", "Risk_Category", "Movement_Quality",
            "Knee_Valgus_Left", "Knee_Valgus_Right", "Knee_Flexion_Min",
            "Trunk_Lateral_Lean", "Pelvic_Drop", "Bilateral_Asymmetry_Pct",
            "Landing_Force_G"
        ])

        for a in assessments:
            b = a.get("biomechanical_metrics", {})
            writer.writerow([
                a.get("id"), a.get("athlete_id"), a.get("athlete_name"), a.get("activity_type"), a.get("created_at", "")[:10],
                a.get("overall_risk_score"), a.get("risk_category"), a.get("movement_quality_score"),
                b.get("knee_valgus_left"), b.get("knee_valgus_right"), b.get("knee_flexion_left"),
                b.get("trunk_lateral_lean"), b.get("hip_stability_drop"), b.get("bilateral_asymmetry_pct"),
                b.get("landing_force_proxy_g")
            ])

        return output.getvalue()

# Singleton
report_generator = ReportGenerator()
