"""
Synthetic Athletic Motion Generator
Creates realistic demonstration video clips with simulated biomechanics
(e.g., Squat with Valgus Collapse, Stiff Jump Landing, Sprint Deceleration).
Allows instant evaluation without requiring external video files.
"""
import math
import cv2
import numpy as np
from pathlib import Path
from backend.config import UPLOAD_DIR

def generate_demo_video(motion_type: str = "valgus_squat", duration_sec: float = 3.0, fps: int = 24) -> Path:
    """
    Renders a realistic sports motion demonstration video clip.
    Supported motion types: 'valgus_squat', 'jump_landing', 'sprint_cut'
    """
    output_filename = f"demo_{motion_type}.mp4"
    output_path = UPLOAD_DIR / output_filename
    
    # If already generated, return cached path
    if output_path.exists() and output_path.stat().st_size > 1000:
        return output_path

    w, h = 640, 480
    # Use avc1 (H.264) for native HTML5 video playback in all web browsers
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (w, h))
    if not out.isOpened():
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (w, h))

    total_frames = int(duration_sec * fps)
    
    for i in range(total_frames):
        t = i / total_frames # 0.0 to 1.0
        frame = np.full((h, w, 3), (25, 27, 34), dtype=np.uint8) # Dark aesthetic floor/gym background

        # Draw sports grid lines on floor
        cv2.line(frame, (0, int(h * 0.85)), (w, int(h * 0.85)), (45, 50, 65), 2)
        cv2.line(frame, (int(w * 0.2), int(h * 0.85)), (int(w * 0.05), h), (40, 45, 60), 2)
        cv2.line(frame, (int(w * 0.8), int(h * 0.85)), (int(w * 0.95), h), (40, 45, 60), 2)

        # Simulation kinematics based on motion_type
        phase = math.sin(t * math.pi * 2) # Cycle -1 to +1
        cx, cy = int(w * 0.5), int(h * 0.45)

        if motion_type == "valgus_squat":
            # Squat depth: hip drops down
            squat_depth = (1.0 - math.cos(t * math.pi * 2)) / 2.0 # 0.0 at top, 1.0 at bottom
            hip_y = int(cy + squat_depth * 85)
            
            # Left knee experiences pronounced medial collapse (Valgus) at bottom of squat
            valgus_collapse = squat_depth * 42 # inward collapse pixels
            knee_y = int(hip_y + 80 + (1.0 - squat_depth) * 20)
            ankle_y = int(h * 0.82)
            
            # Key coordinates
            head = (cx, int(hip_y - 120))
            sh_l = (cx - 45, int(hip_y - 80))
            sh_r = (cx + 45, int(hip_y - 80))
            hip_l = (cx - 30, hip_y)
            hip_r = (cx + 30, hip_y)
            
            # Valgus: Left knee pulls medially inwards towards center
            knee_l = (int(cx - 35 + valgus_collapse), knee_y)
            knee_r = (cx + 40, knee_y) # Right knee tracks normally
            
            ankle_l = (cx - 50, ankle_y)
            ankle_r = (cx + 50, ankle_y)

        elif motion_type == "jump_landing":
            # High jump and rapid stiff landing impact
            if t < 0.4: # Airborne
                jump_height = math.sin((t / 0.4) * math.pi) * 90
                hip_y = int(cy - jump_height)
                knee_y = int(hip_y + 75)
                ankle_y = int(knee_y + 65)
            else: # Landing & impact phase
                land_t = (t - 0.4) / 0.6
                stiff_sink = math.sin(land_t * math.pi) * 25 # Very low flexion = stiff impact!
                hip_y = int(cy + 30 + stiff_sink)
                knee_y = int(hip_y + 75)
                ankle_y = int(h * 0.82)

            head = (cx, int(hip_y - 120))
            sh_l, sh_r = (cx - 45, int(hip_y - 80)), (cx + 45, int(hip_y - 80))
            hip_l, hip_r = (cx - 30, hip_y), (cx + 30, hip_y)
            knee_l, knee_r = (cx - 32, knee_y), (cx + 32, knee_y)
            ankle_l, ankle_r = (cx - 45, ankle_y), (cx + 45, ankle_y)

        else: # sprint_cut
            # Lateral cutting step with trunk lateral lean
            sway = math.sin(t * math.pi * 3) * 45
            hip_y = int(cy + 40)
            head = (int(cx + sway * 1.3), int(hip_y - 120))
            sh_l = (int(cx + sway - 40), int(hip_y - 80))
            sh_r = (int(cx + sway + 40), int(hip_y - 80))
            hip_l = (int(cx + sway * 0.5 - 30), hip_y)
            hip_r = (int(cx + sway * 0.5 + 30), hip_y)
            knee_l = (int(cx - 40), int(hip_y + 75))
            knee_r = (int(cx + 40), int(hip_y + 75))
            ankle_l = (int(cx - 55), int(h * 0.82))
            ankle_r = (int(cx + 55), int(h * 0.82))

        # Render athlete figure
        # Head
        cv2.circle(frame, head, 18, (210, 220, 240), -1, cv2.LINE_AA)
        cv2.circle(frame, head, 18, (60, 80, 120), 2, cv2.LINE_AA)

        # Torso
        cv2.line(frame, head, ((hip_l[0] + hip_r[0]) // 2, (hip_l[1] + hip_r[1]) // 2), (200, 210, 230), 10, cv2.LINE_AA)
        cv2.line(frame, sh_l, sh_r, (180, 190, 210), 8, cv2.LINE_AA)
        cv2.line(frame, hip_l, hip_r, (180, 190, 210), 8, cv2.LINE_AA)

        # Arms
        cv2.line(frame, sh_l, (sh_l[0] - 25, sh_l[1] + 45), (170, 180, 200), 6, cv2.LINE_AA)
        cv2.line(frame, sh_r, (sh_r[0] + 25, sh_r[1] + 45), (170, 180, 200), 6, cv2.LINE_AA)

        # Legs
        cv2.line(frame, hip_l, knee_l, (190, 205, 230), 8, cv2.LINE_AA)
        cv2.line(frame, knee_l, ankle_l, (190, 205, 230), 7, cv2.LINE_AA)
        cv2.line(frame, hip_r, knee_r, (190, 205, 230), 8, cv2.LINE_AA)
        cv2.line(frame, knee_r, ankle_r, (190, 205, 230), 7, cv2.LINE_AA)

        # Athletic shoes
        cv2.ellipse(frame, ankle_l, (14, 6), 0, 0, 360, (0, 215, 255), -1, cv2.LINE_AA)
        cv2.ellipse(frame, ankle_r, (14, 6), 0, 0, 360, (0, 215, 255), -1, cv2.LINE_AA)

        # Overlay activity banner
        label = f"DEMO SIMULATION: {motion_type.upper().replace('_', ' ')} (Frame {i+1}/{total_frames})"
        cv2.putText(frame, label, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 220, 255), 2, cv2.LINE_AA)

        out.write(frame)

    out.release()
    print(f"[SyntheticMotion] Rendered demo video: {output_path}")
    return output_path
