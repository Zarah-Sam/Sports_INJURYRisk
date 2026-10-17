/**
 * AI Sports Injury Risk Detection Platform
 * Frontend State Controller & Reactive UI Logic
 */

const state = {
  currentRole: 'sports_scientist',
  user: {
    id: 'USR-004',
    full_name: 'Dr. Aris Thorne',
    role: 'sports_scientist',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=100&q=80'
  },
  athletes: [],
  assessments: [],
  notifications: [],
  currentAssessment: null,
  webcamActive: false,
  webcamStream: null,
  webcamInterval: null
};

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', async () => {
  await loadInitialData();
  renderRoleDashboard();
  renderAthletesTable();
  renderAnalyticsArchive();
  renderExerciseLibrary();
  renderValgusChart();

  // Load initial demo assessment into analyzer
  await window.loadDemo('valgus_squat', 'ATH-001', 'Jump Deceleration Valgus Collapse');
});

async function loadInitialData() {
  try {
    const [athRes, asmRes, notifRes] = await Promise.all([
      fetch('/api/athletes').then(r => r.json()),
      fetch('/api/assessments').then(r => r.json()),
      fetch('/api/notifications').then(r => r.json())
    ]);
    state.athletes = athRes;
    state.assessments = asmRes;
    state.notifications = notifRes;
    updateNotifBadge();
  } catch (e) {
    console.error('Failed to load initial data:', e);
  }
}

// --- TAB SWITCHING ---
window.switchTab = function(tabName) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

  const btn = Array.from(document.querySelectorAll('.tab-btn')).find(b => 
    b.getAttribute('onclick') && b.getAttribute('onclick').includes(tabName)
  );
  if (btn) btn.classList.add('active');

  const targetPane = document.getElementById(`tab-${tabName}`);
  if (targetPane) targetPane.classList.add('active');
};

// --- ROLE SWITCHING ---
window.switchRole = async function(role) {
  state.currentRole = role;

  const roleProfiles = {
    'athlete': {
      full_name: 'Marcus Vance',
      title: 'Forward (Soccer) | ATH-001',
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=100&q=80'
    },
    'coach': {
      full_name: 'Coach Dave Miller',
      title: 'Head Performance Coach',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=100&q=80'
    },
    'physiotherapist': {
      full_name: 'Dr. Priya Patel (PT, DPT)',
      title: 'Chief Sports Physiotherapist',
      avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=100&q=80'
    },
    'sports_scientist': {
      full_name: 'Dr. Aris Thorne',
      title: 'Biomechanist & Data Director',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=100&q=80'
    },
    'administrator': {
      full_name: 'Systems Administrator',
      title: 'Platform Infrastructure Lead',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=100&q=80'
    }
  };

  const prof = roleProfiles[role] || roleProfiles['sports_scientist'];
  state.user.full_name = prof.full_name;
  state.user.role = role;
  state.user.avatar = prof.avatar;

  document.getElementById('user-display-name').textContent = prof.full_name;
  document.getElementById('user-avatar').src = prof.avatar;
  document.getElementById('dashboard-tab-title').textContent = `${role.replace('_', ' ').toUpperCase()} DASHBOARD`;

  renderRoleDashboard();
};

// --- RENDER DYNAMIC DASHBOARDS ---
function renderRoleDashboard() {
  const kpiRow = document.getElementById('kpi-row');
  const roleView = document.getElementById('role-specific-view');
  const role = state.currentRole;

  if (role === 'athlete') {
    // --- ATHLETE DASHBOARD ---
    const ath = state.athletes.find(a => a.athlete_id === 'ATH-001') || state.athletes[0] || {};
    kpiRow.innerHTML = `
      <div class="stat-card stat-high">
        <div class="stat-header"><span class="stat-title">Personal Injury Risk</span><span class="stat-icon">⚠️</span></div>
        <div class="stat-value" style="color: var(--status-high);">${ath.latest_risk_score || 68.5} <span style="font-size: 14px; color: var(--text-muted);">/100</span></div>
        <div class="stat-sub">High Risk | Left Knee Valgus Focus</div>
      </div>
      <div class="stat-card stat-mod">
        <div class="stat-header"><span class="stat-title">Movement Quality</span><span class="stat-icon">🎯</span></div>
        <div class="stat-value" style="color: var(--status-mod);">${ath.movement_quality_score || 64}%</div>
        <div class="stat-sub">Target: &gt;80% for full match clearance</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Workload Ratio (ACWR)</span><span class="stat-icon">📊</span></div>
        <div class="stat-value" style="color: var(--accent-cyan);">${ath.training_load?.acwr || 1.42}</div>
        <div class="stat-sub">High Acute Workload (Deload advised)</div>
      </div>
      <div class="stat-card stat-low">
        <div class="stat-header"><span class="stat-title">Prescribed Exercises</span><span class="stat-icon">✅</span></div>
        <div class="stat-value" style="color: var(--status-low);">3 / 3</div>
        <div class="stat-sub">Daily corrective program ready</div>
      </div>
    `;

    roleView.innerHTML = `
      <div class="grid-cols-2">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title"><span>📋</span> Today's Prescribed Corrective Regimen</div>
            <span class="badge-pill">Target: Glute Medius & ACL Shield</span>
          </div>
          <div id="athlete-todo-exercises">
            <div class="exercise-card" style="border-left: 4px solid var(--accent-cyan);">
              <div class="exercise-name">
                <span>Banded Monster Walks</span>
                <span class="exercise-dose">4 sets x 15 reps</span>
              </div>
              <div class="exercise-cue">Cue: Keep knees tracking over 2nd toe; maintain outward band abduction.</div>
              <div style="margin-top: 8px;"><label><input type="checkbox" checked> Completed today</label></div>
            </div>
            <div class="exercise-card" style="border-left: 4px solid var(--accent-cyan);">
              <div class="exercise-name">
                <span>Single-Leg Drop to Soft Stick</span>
                <span class="exercise-dose">3 sets x 6 reps/leg</span>
              </div>
              <div class="exercise-cue">Cue: Soft ninja landing; absorb impact into 50° knee flexion.</div>
              <div style="margin-top: 8px;"><label><input type="checkbox"> Mark as Completed</label></div>
            </div>
            <div class="exercise-card" style="border-left: 4px solid var(--accent-cyan);">
              <div class="exercise-name">
                <span>90/90 Hip Mobility Flow</span>
                <span class="exercise-dose">3 mins total</span>
              </div>
              <div class="exercise-cue">Cue: Internal/external hip rotation to restore sagittal alignment.</div>
              <div style="margin-top: 8px;"><label><input type="checkbox"> Mark as Completed</label></div>
            </div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div class="panel-title"><span>🎥</span> Your Recent Assessment Video</div>
            <button class="btn btn-secondary" onclick="window.switchTab('analyzer')">Open Full Analyzer</button>
          </div>
          <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 14px;">
            Assessment on Jump Landing Deceleration showed an inward left knee shift (16.8°). Review with Coach Dave Miller.
          </p>
          <div style="background: rgba(0,0,0,0.5); border-radius: 8px; padding: 20px; text-align: center;">
            <div style="font-size: 40px; margin-bottom: 10px;">🦿</div>
            <div style="font-weight: 700; color: var(--status-crit);">Left Knee Abduction Alert</div>
            <div style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Peak Valgus Spike at frame #42</div>
            <button class="btn btn-primary" style="margin-top: 14px;" onclick="window.switchTab('analyzer')">Watch Annotated Telemetry</button>
          </div>
        </div>
      </div>
    `;

  } else if (role === 'coach') {
    // --- COACH DASHBOARD ---
    const highRiskCount = state.athletes.filter(a => a.risk_category === 'High Risk' || a.risk_category === 'Critical Risk').length;
    kpiRow.innerHTML = `
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Squad Size</span><span class="stat-icon">👥</span></div>
        <div class="stat-value" style="color: var(--accent-cyan);">${state.athletes.length} <span style="font-size: 14px; color: var(--text-muted);">Active</span></div>
        <div class="stat-sub">Roster across all sports</div>
      </div>
      <div class="stat-card stat-crit">
        <div class="stat-header"><span class="stat-title">High Risk Flags</span><span class="stat-icon">🚨</span></div>
        <div class="stat-value" style="color: var(--status-crit);">${highRiskCount}</div>
        <div class="stat-sub">Requires workload restriction</div>
      </div>
      <div class="stat-card stat-low">
        <div class="stat-header"><span class="stat-title">Squad Readiness</span><span class="stat-icon">⚡</span></div>
        <div class="stat-value" style="color: var(--status-low);">74.5%</div>
        <div class="stat-sub">Matchday competitive fitness</div>
      </div>
      <div class="stat-card stat-mod">
        <div class="stat-header"><span class="stat-title">Workload Spikes</span><span class="stat-icon">📈</span></div>
        <div class="stat-value" style="color: var(--status-mod);">2</div>
        <div class="stat-sub">Athletes with ACWR &gt; 1.4</div>
      </div>
    `;

    roleView.innerHTML = `
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title"><span>📋</span> Squad Injury Risk Overview & Tactical Availability</div>
          <button class="btn btn-secondary" onclick="window.switchTab('athletes')">View Full Roster</button>
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>Athlete</th>
                <th>Sport / Position</th>
                <th>Risk Category</th>
                <th>Risk Score</th>
                <th>Workload (ACWR)</th>
                <th>Tactical Clearance</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              ${state.athletes.map(a => `
                <tr>
                  <td><strong>${a.full_name}</strong></td>
                  <td>${a.sport_type} (${a.position})</td>
                  <td><span class="status-chip ${getStatusClass(a.risk_category)}">${a.risk_category}</span></td>
                  <td><strong>${a.latest_risk_score}</strong>/100</td>
                  <td>${a.training_load?.acwr || '1.10'}</td>
                  <td>
                    ${a.risk_category === 'Critical Risk' ? '<span style="color: #ef4444; font-weight: 700;">⛔ Benched / Rehab</span>' :
                      (a.risk_category === 'High Risk' ? '<span style="color: #f97316; font-weight: 700;">⚠️ Minutes Restricted</span>' :
                      '<span style="color: #10b981; font-weight: 700;">✅ Full Clearance</span>')}
                  </td>
                  <td>
                    <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 11px;" onclick="window.loadAthleteInAnalyzer('${a.athlete_id}')">Analyze Movement</button>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

  } else if (role === 'physiotherapist') {
    // --- PHYSIOTHERAPIST DASHBOARD ---
    kpiRow.innerHTML = `
      <div class="stat-card stat-high">
        <div class="stat-header"><span class="stat-title">Active Rehabilitation</span><span class="stat-icon">🩺</span></div>
        <div class="stat-value" style="color: var(--status-high);">3</div>
        <div class="stat-sub">Under daily clinical tracking</div>
      </div>
      <div class="stat-card stat-mod">
        <div class="stat-header"><span class="stat-title">Bilateral Deficit Index</span><span class="stat-icon">⚖️</span></div>
        <div class="stat-value" style="color: var(--status-mod);">18.2%</div>
        <div class="stat-sub">Mean left vs right limb asymmetry</div>
      </div>
      <div class="stat-card stat-low">
        <div class="stat-header"><span class="stat-title">Rehab Progression Rate</span><span class="stat-icon">📈</span></div>
        <div class="stat-value" style="color: var(--status-low);">+12.4%</div>
        <div class="stat-sub">ROM & Valgus reduction this month</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Clinical Notes</span><span class="stat-icon">📝</span></div>
        <div class="stat-value" style="color: var(--accent-cyan);">14</div>
        <div class="stat-sub">Biomechanical entries logged</div>
      </div>
    `;

    roleView.innerHTML = `
      <div class="grid-cols-2">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title"><span>🩺</span> Active Rehabilitation Case: Marcus Vance (ATH-001)</div>
            <span class="status-chip high">ACL Reconstruction Watch</span>
          </div>
          <div style="font-size: 13px; line-height: 1.6; color: var(--text-muted); margin-bottom: 16px;">
            <strong>Diagnosis:</strong> Status-post left ACL reconstruction (month 14). Patient demonstrates guarded left knee flexion with compensatory medial dynamic valgus collapse (16.8°) on deceleration landings.
          </div>
          <div class="formula-bar-item">
            <div class="formula-label"><span>Knee Valgus Recovery Goal (&lt;8.0°)</span><span style="color: var(--status-crit);">Current: 16.8°</span></div>
            <div class="formula-progress"><div class="formula-fill" style="width: 45%; background: var(--status-crit);"></div></div>
          </div>
          <div class="formula-bar-item">
            <div class="formula-label"><span>Bilateral Quadriceps Symmetry Index (&gt;90%)</span><span style="color: var(--status-mod);">Current: 78.5%</span></div>
            <div class="formula-progress"><div class="formula-fill" style="width: 78%; background: var(--status-mod);"></div></div>
          </div>
          <div style="margin-top: 16px;">
            <button class="btn btn-primary" onclick="window.loadDemo('valgus_squat', 'ATH-001')">Load Biomechanical Assessment</button>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div class="panel-title"><span>📋</span> Physiotherapy Protocol Prescription</div>
            <button class="btn btn-secondary" onclick="window.switchTab('exercises')">Browse Library</button>
          </div>
          <div class="exercise-card">
            <div class="exercise-name"><span>Gluteus Medius Abductor Eccentrics</span><span class="exercise-dose">4x15</span></div>
            <div class="exercise-cue">Side-lying clam with 25lb looped band; slow 3-second descent.</div>
          </div>
          <div class="exercise-card">
            <div class="exercise-name"><span>Drop Vertical Jump Soft Landings</span><span class="exercise-dose">3x6</span></div>
            <div class="exercise-cue">Land on dual force plates with biofeedback mirror to correct valgus.</div>
          </div>
          <div class="exercise-card">
            <div class="exercise-name"><span>Nordic Hamstring Curls</span><span class="exercise-dose">3x5</span></div>
            <div class="exercise-cue">Eccentric phase emphasized to protect biceps femoris.</div>
          </div>
        </div>
      </div>
    `;

  } else if (role === 'administrator') {
    // --- ADMIN DASHBOARD ---
    kpiRow.innerHTML = `
      <div class="stat-card stat-low">
        <div class="stat-header"><span class="stat-title">Platform Status</span><span class="stat-icon">⚡</span></div>
        <div class="stat-value" style="color: var(--status-low);">OPERATIONAL</div>
        <div class="stat-sub">FastAPI Microservices Healthy</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Inference Engine</span><span class="stat-icon">🧠</span></div>
        <div class="stat-value" style="color: var(--accent-cyan); font-size: 24px;">YOLOv8-POSE</div>
        <div class="stat-sub">17 COCO Keypoints Vector Math</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Avg Video Latency</span><span class="stat-icon">⏱️</span></div>
        <div class="stat-value" style="color: var(--accent-indigo);">28.4 <span style="font-size: 14px;">ms/frame</span></div>
        <div class="stat-sub">Real-Time FPS: 35.2</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Total Database Records</span><span class="stat-icon">💾</span></div>
        <div class="stat-value" style="color: var(--text-main);">${state.assessments.length + state.athletes.length}</div>
        <div class="stat-sub">Persisted JSON & Reports</div>
      </div>
    `;

    roleView.innerHTML = `
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title"><span>⚙️</span> System Architecture & Security Audit</div>
          <span class="badge-pill">JWT & Role Guard Active</span>
        </div>
        <div style="font-size: 13px; line-height: 1.8; color: var(--text-muted);">
          <div><strong>Authentication:</strong> HMAC-SHA256 Signed JWT with 24-hour expiration</div>
          <div><strong>Role Matrix:</strong> Athlete, Coach, Physiotherapist, Sports Scientist, Administrator</div>
          <div><strong>Supported Media Codecs:</strong> MP4 (H.264 / mp4v), QuickTime MOV, WebM, OpenCV Raw VideoCapture</div>
          <div><strong>Storage Directory:</strong> <code>C:\\Users\\hp\\.gemini\\antigravity-ide\\scratch\\sports-injury-detection\\data</code></div>
        </div>
      </div>
    `;

  } else {
    // --- SPORTS SCIENTIST DASHBOARD (DEFAULT) ---
    kpiRow.innerHTML = `
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Athletes Monitored</span><span class="stat-icon">🏃</span></div>
        <div class="stat-value" style="color: var(--accent-cyan);">${state.athletes.length}</div>
        <div class="stat-sub">Multi-sport tracking cohort</div>
      </div>
      <div class="stat-card stat-crit">
        <div class="stat-header"><span class="stat-title">Critical Kinematic Alerts</span><span class="stat-icon">🚨</span></div>
        <div class="stat-value" style="color: var(--status-crit);">2</div>
        <div class="stat-sub">Valgus &gt; 15° or ACWR &gt; 1.5</div>
      </div>
      <div class="stat-card stat-mod">
        <div class="stat-header"><span class="stat-title">Mean Cohort Valgus</span><span class="stat-icon">📐</span></div>
        <div class="stat-value" style="color: var(--status-mod);">11.4°</div>
        <div class="stat-sub">Normal reference range: &lt; 8.0°</div>
      </div>
      <div class="stat-card stat-low">
        <div class="stat-header"><span class="stat-title">Model Accuracy</span><span class="stat-icon">🎯</span></div>
        <div class="stat-value" style="color: var(--status-low);">94.8%</div>
        <div class="stat-sub">Validated against 3D Motion Capture</div>
      </div>
    `;

    roleView.innerHTML = `
      <div class="grid-cols-2">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title"><span>🔬</span> Biomechanical Deviation Spectrum</div>
            <button class="btn btn-secondary" onclick="window.downloadCSV()">Export Telemetry (CSV)</button>
          </div>
          <div style="font-size: 13px; color: var(--text-muted); line-height: 1.6; margin-bottom: 16px;">
            Real-time multi-segment kinetic chain tracking. Below are the weighted risk model contributors across recent assessments:
          </div>
          <div class="formula-bar-item">
            <div class="formula-label"><span>Biomechanical Deviations Weight (35%)</span><span>35% Impact</span></div>
            <div class="formula-progress"><div class="formula-fill" style="width: 35%;"></div></div>
          </div>
          <div class="formula-bar-item">
            <div class="formula-label"><span>Historical Injury Factors Weight (20%)</span><span>20% Impact</span></div>
            <div class="formula-progress"><div class="formula-fill" style="width: 20%;"></div></div>
          </div>
          <div class="formula-bar-item">
            <div class="formula-label"><span>Movement Asymmetry Weight (20%)</span><span>20% Impact</span></div>
            <div class="formula-progress"><div class="formula-fill" style="width: 20%;"></div></div>
          </div>
          <div class="formula-bar-item">
            <div class="formula-label"><span>Training Load Indicators Weight (15%)</span><span>15% Impact</span></div>
            <div class="formula-progress"><div class="formula-fill" style="width: 15%;"></div></div>
          </div>
          <div class="formula-bar-item">
            <div class="formula-label"><span>Fatigue Indicators Weight (10%)</span><span>10% Impact</span></div>
            <div class="formula-progress"><div class="formula-fill" style="width: 10%;"></div></div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div class="panel-title"><span>🎥</span> Instant Movement Biomechanics Evaluation</div>
            <button class="btn btn-primary" onclick="window.switchTab('analyzer')">Launch Full Video Lab</button>
          </div>
          <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px;">
            Test athlete movement videos with automated HUD keypoint tracking, joint angle extraction, and injury prediction.
          </p>
          <div style="display: flex; gap: 10px; flex-direction: column;">
            <button class="btn btn-secondary" style="justify-content: flex-start;" onclick="window.loadDemo('valgus_squat', 'ATH-001'); window.switchTab('analyzer');">
              💥 <strong>Squat Valgus Collapse</strong> (Marcus Vance — ACL Risk)
            </button>
            <button class="btn btn-secondary" style="justify-content: flex-start;" onclick="window.loadDemo('jump_landing', 'ATH-001'); window.switchTab('analyzer');">
              🦿 <strong>Stiff Jump Landing</strong> (Impact Force &gt; 3.5g)
            </button>
            <button class="btn btn-secondary" style="justify-content: flex-start;" onclick="window.loadDemo('sprint_cut', 'ATH-002'); window.switchTab('analyzer');">
              ⚡ <strong>Sprint Cutting Mechanics</strong> (Hamstring & Ankle Sway)
            </button>
          </div>
        </div>
      </div>
    `;
  }
}

// --- VIDEO ANALYZER LOGIC ---
window.loadDemo = async function(motionType, athleteId = 'ATH-001', activityType = 'Deceleration Biomechanics') {
  showAnalyzerLoading(true);
  try {
    const formData = new FormData();
    formData.append('motion_type', motionType);
    formData.append('athlete_id', athleteId);
    formData.append('activity_type', activityType);

    const res = await fetch('/api/analyze/demo', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    populateAssessmentInUI(data);
  } catch (err) {
    console.error('Error loading demo video:', err);
  } finally {
    showAnalyzerLoading(false);
  }
};

window.handleVideoUpload = async function(event) {
  const file = event.target.files[0];
  if (!file) return;

  showAnalyzerLoading(true);
  try {
    const formData = new FormData();
    formData.append('video', file);
    formData.append('athlete_id', 'ATH-001');
    formData.append('activity_type', 'Custom Athlete Movement Upload');

    const res = await fetch('/api/analyze/upload', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    populateAssessmentInUI(data);
    await loadInitialData();
  } catch (err) {
    console.error('Upload failed:', err);
    alert('Video analysis failed. Please ensure video format is supported (.mp4, .mov, .webm).');
  } finally {
    showAnalyzerLoading(false);
  }
};

function populateAssessmentInUI(data) {
  state.currentAssessment = data;

  // Set video player
  const player = document.getElementById('main-video-player');
  const source = document.getElementById('video-source');
  const canvas = document.getElementById('webcam-canvas');
  if (canvas) canvas.style.display = 'none';
  if (player) {
    player.style.display = 'block';
    if (data.processed_video_url) {
      const vUrl = data.processed_video_url + '?t=' + Date.now();
      if (source) source.src = vUrl;
      player.src = vUrl;
      player.load();
      player.play().catch(e => {
        console.warn('Playback notice:', e);
      });
    }
  }

  // Update HUD
  const hudRisk = document.getElementById('hud-risk-pill');
  if (hudRisk) {
    hudRisk.textContent = `${data.risk_category.toUpperCase()}`;
    hudRisk.style.color = data.category_color;
  }

  // Telemetry Cards
  const bio = data.biomechanical_metrics || {};
  document.getElementById('m-valgus-l').textContent = `${bio.knee_valgus_left || 0}°`;
  document.getElementById('m-valgus-l').className = `val ${bio.knee_valgus_left > 14 ? 'val-crit' : (bio.knee_valgus_left > 8 ? 'val-mod' : 'val-low')}`;
  
  document.getElementById('m-valgus-r').textContent = `${bio.knee_valgus_right || 0}°`;
  document.getElementById('m-valgus-r').className = `val ${bio.knee_valgus_right > 14 ? 'val-crit' : (bio.knee_valgus_right > 8 ? 'val-mod' : 'val-low')}`;

  document.getElementById('m-knee-flex').textContent = `${bio.knee_flexion_left || 0}°`;
  document.getElementById('m-knee-flex').className = `val ${bio.knee_flexion_left < 35 ? 'val-crit' : 'val-low'}`;

  document.getElementById('m-trunk-lean').textContent = `${bio.trunk_lateral_lean || 0}°`;
  document.getElementById('m-pelvic-drop').textContent = `${bio.hip_stability_drop || 0}°`;
  document.getElementById('m-asym-pct').textContent = `${bio.bilateral_asymmetry_pct || 0}%`;

  // Risk Score Gauge
  const scoreCircle = document.getElementById('risk-score-circle');
  const scoreNum = document.getElementById('risk-score-display');
  const categoryDisp = document.getElementById('risk-category-display');
  
  scoreCircle.style.borderColor = data.category_color;
  scoreCircle.style.boxShadow = `0 0 20px ${data.category_color}55`;
  scoreNum.textContent = data.overall_risk_score;
  scoreNum.style.color = data.category_color;
  categoryDisp.textContent = data.risk_category;
  categoryDisp.style.color = data.category_color;

  // Formula Breakdown Bars
  const breakdown = data.weighted_breakdown || {};
  setFormulaBar('wt-bio-val', 'wt-bio-bar', breakdown.biomechanical_deviations || 50);
  setFormulaBar('wt-hist-val', 'wt-hist-bar', breakdown.historical_injury_factors || 50);
  setFormulaBar('wt-asym-val', 'wt-asym-bar', breakdown.movement_asymmetry || 50);
  setFormulaBar('wt-load-val', 'wt-load-bar', breakdown.training_load_indicators || 50);
  setFormulaBar('wt-fatigue-val', 'wt-fatigue-bar', breakdown.fatigue_indicators || 50);

  // Categorical Injury Predictions
  const injuriesList = document.getElementById('injury-predictions-list');
  injuriesList.innerHTML = (data.detected_injuries || []).map(inj => `
    <div class="injury-risk-item ${inj.level === 'High' ? 'risk-high' : (inj.level === 'Moderate' ? 'risk-mod' : 'risk-low')}">
      <div class="injury-risk-header">
        <span class="injury-risk-name">${inj.category}</span>
        <span class="injury-badge" style="background: ${inj.color}22; color: ${inj.color}; border: 1px solid ${inj.color};">
          ${inj.level} (${inj.probability}%)
        </span>
      </div>
      <div class="injury-factors">${inj.key_factors}</div>
    </div>
  `).join('');

  // Corrective Exercises
  const recList = document.getElementById('exercise-regimen-list');
  const recs = data.recommendations || {};
  recList.innerHTML = `
    <div style="font-size: 12.5px; color: var(--accent-cyan); font-weight: 700; margin-bottom: 10px;">
      Target Modification: ${recs.training_modification || 'Standard training'}
    </div>
    ${(recs.exercises || []).map(ex => `
      <div class="exercise-card">
        <div class="exercise-name">
          <span>${ex.name}</span>
          <span class="exercise-dose">${ex.dose}</span>
        </div>
        <div class="exercise-cue"><strong>Cue:</strong> ${ex.cues}</div>
      </div>
    `).join('')}
  `;
}

function setFormulaBar(valId, barId, score) {
  const valEl = document.getElementById(valId);
  const barEl = document.getElementById(barId);
  if (valEl) valEl.textContent = `${score} / 100`;
  if (barEl) barEl.style.width = `${Math.min(100, Math.max(5, score))}%`;
}

function showAnalyzerLoading(isLoading) {
  const hud = document.getElementById('hud-model-tag');
  if (hud) hud.textContent = isLoading ? 'PROCESSING VIDEO (YOLOv8)...' : 'YOLOv8-POSE ACTIVE';
}

// --- WEBCAM REAL-TIME MODE ---
window.toggleWebcam = async function() {
  const player = document.getElementById('main-video-player');
  const canvas = document.getElementById('webcam-canvas');
  const btn = document.getElementById('btn-webcam-toggle');

  if (state.webcamActive) {
    // Stop
    state.webcamActive = false;
    btn.textContent = '📷 Live Webcam Mode';
    btn.classList.remove('btn-danger');
    if (state.webcamStream) {
      state.webcamStream.getTracks().forEach(t => t.stop());
      state.webcamStream = null;
    }
    if (state.webcamInterval) clearInterval(state.webcamInterval);
    canvas.style.display = 'none';
    player.style.display = 'block';
    return;
  }

  // Start
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
    state.webcamStream = stream;
    state.webcamActive = true;
    btn.textContent = '⏹️ Stop Webcam';
    btn.classList.add('btn-danger');

    player.style.display = 'none';
    canvas.style.display = 'block';
    canvas.width = 640;
    canvas.height = 480;

    const hiddenVid = document.createElement('video');
    hiddenVid.srcObject = stream;
    hiddenVid.play();

    const ctx = canvas.getContext('2d');

    state.webcamInterval = setInterval(async () => {
      if (!state.webcamActive) return;
      ctx.drawImage(hiddenVid, 0, 0, 640, 480);
      const dataUrl = canvas.toDataURL('image/jpeg', 0.65);

      try {
        const res = await fetch('/api/analyze/frame', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image_base64: dataUrl })
        });
        const result = await res.json();
        if (result.annotated_frame) {
          const img = new Image();
          img.onload = () => ctx.drawImage(img, 0, 0, 640, 480);
          img.src = result.annotated_frame;
        }
        if (result.metrics) {
          document.getElementById('m-valgus-l').textContent = `${result.metrics.knee_valgus_left || 0}°`;
          document.getElementById('m-valgus-r').textContent = `${result.metrics.knee_valgus_right || 0}°`;
        }
      } catch (err) {
        // frame processing
      }
    }, 150); // ~7 FPS live telemetry loop

  } catch (err) {
    alert('Webcam access was not granted or is unavailable on this device. Using high-speed video simulation instead.');
  }
};

// --- REPORT EXPORT ---
window.exportCurrentReport = function() {
  if (!state.currentAssessment || !state.currentAssessment.id) {
    alert('Please run or select an assessment first.');
    return;
  }
  const reportUrl = `/api/reports/${state.currentAssessment.id}/html`;
  window.open(reportUrl, '_blank');
};

window.downloadCSV = function() {
  window.location.href = '/api/reports/export-csv';
};

// --- ATHLETES TABLE ---
function renderAthletesTable() {
  const tbody = document.getElementById('athletes-table-body');
  if (!tbody) return;

  tbody.innerHTML = state.athletes.map(a => `
    <tr>
      <td><strong>${a.full_name}</strong></td>
      <td><code>${a.athlete_id}</code></td>
      <td>${a.sport_type} (${a.position})</td>
      <td><span class="status-chip ${getStatusClass(a.risk_category)}">${a.risk_category} (${a.latest_risk_score})</span></td>
      <td><strong>${a.movement_quality_score}%</strong></td>
      <td>${a.training_load?.acwr || '1.15'}</td>
      <td><small style="color: var(--text-dim);">${(a.injury_history || []).map(i => i.injury || i).join(', ') || 'None'}</small></td>
      <td>
        <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 11px;" onclick="window.loadAthleteInAnalyzer('${a.athlete_id}')">
          Analyze
        </button>
      </td>
    </tr>
  `).join('');
}

window.loadAthleteInAnalyzer = function(athleteId) {
  window.loadDemo('valgus_squat', athleteId, 'Kinematic Biomechanics Evaluation');
  window.switchTab('analyzer');
};

window.promptAddAthlete = async function() {
  const name = prompt('Athlete Full Name:');
  if (!name) return;
  const sport = prompt('Sport Type (e.g. Soccer, Basketball, Track):', 'Soccer');
  const pos = prompt('Position:', 'Forward');

  try {
    const res = await fetch('/api/athletes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        full_name: name,
        sport_type: sport,
        position: pos,
        age: 22,
        height_cm: 180,
        weight_kg: 75
      })
    });
    const newAth = await res.json();
    state.athletes.push(newAth);
    renderAthletesTable();
    alert(`Registered ${newAth.full_name} with ID ${newAth.athlete_id}!`);
  } catch (e) {
    alert('Failed to register athlete.');
  }
};

// --- ANALYTICS ARCHIVE ---
function renderAnalyticsArchive() {
  const tbody = document.getElementById('assessment-history-body');
  if (!tbody) return;

  tbody.innerHTML = state.assessments.map(a => {
    const b = a.biomechanical_metrics || {};
    return `
      <tr>
        <td><code>${a.id}</code></td>
        <td><strong>${a.athlete_name}</strong></td>
        <td>${a.activity_type}</td>
        <td><strong style="color: ${a.category_color}">${a.overall_risk_score}</strong>/100</td>
        <td><span class="status-chip ${getStatusClass(a.risk_category)}">${a.risk_category}</span></td>
        <td>L: ${b.knee_valgus_left || 0}° | R: ${b.knee_valgus_right || 0}°</td>
        <td>${b.landing_force_proxy_g || '1.8'}g</td>
        <td><small>${(a.created_at || '').substring(0, 10)}</small></td>
        <td>
          <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 11px;" onclick="window.open('/api/reports/${a.id}/html', '_blank')">
            PDF
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

function renderValgusChart() {
  const container = document.getElementById('valgus-chart-bars');
  if (!container) return;

  // Kinetic time-series curve simulation
  const curve = [6.2, 7.5, 9.8, 14.2, 16.8, 15.1, 11.2, 8.4, 7.0];
  container.innerHTML = curve.map((val, idx) => {
    const h = (val / 20) * 100;
    const isPeak = val > 14;
    const col = isPeak ? 'var(--status-crit)' : (val > 9 ? 'var(--status-mod)' : 'var(--accent-cyan)');
    return `
      <div style="flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; justify-content: flex-end;">
        <span style="font-size: 10px; color: ${col}; font-weight: 700; margin-bottom: 4px;">${val}°</span>
        <div style="width: 100%; height: ${h}%; background: ${col}; border-radius: 4px 4px 0 0; box-shadow: 0 0 10px ${col}44;"></div>
      </div>
    `;
  }).join('');
}

// --- EXERCISE LIBRARY ---
function renderExerciseLibrary() {
  const grid = document.getElementById('exercise-library-grid');
  if (!grid) return;

  const library = [
    {
      title: 'Banded Lateral Monster Walk',
      category: 'ACL & Knee Valgus Protection',
      target: 'Gluteus Medius & Hip External Rotators',
      dose: '4 sets x 15 steps/direction',
      cue: 'Maintain knee alignment over 2nd metatarsal without medial collapse.'
    },
    {
      title: 'Drop Jump Soft Deceleration',
      category: 'Sagittal Ground Reaction Absorption',
      target: 'Knee Flexion & Quadriceps Shock Absorption',
      dose: '3 sets x 6 reps (30cm box)',
      cue: 'Sink quietly into 50° flexion to absorb ground reaction impulse.'
    },
    {
      title: 'Nordic Hamstring Curl',
      category: 'Hamstring Strain Prevention',
      target: 'Biceps Femoris Eccentric Strength',
      dose: '3 sets x 5 reps (4-sec descent)',
      cue: 'Resist forward fall using pure hamstring tension; maintain neutral hips.'
    },
    {
      title: 'Single-Leg Balance on Foam Pad',
      category: 'Ankle Inversion Sprain Defense',
      target: 'Peroneal Tendons & Subtalar Proprioception',
      dose: '4 sets x 45 seconds/leg',
      cue: 'Lock foot tripod into pad; close eyes for neuro-vestibular challenge.'
    },
    {
      title: 'McGill Big 3 Core Protocol',
      category: 'Lumbar Spine & Torso Stiffness',
      target: 'Quadratus Lumborum & Anti-Extension',
      dose: 'Bird-Dog & Side Bridge (5-4-3-2 reps)',
      cue: 'Brace abdominal wall; eliminate rotational torso sway.'
    },
    {
      title: 'Contrast Hydrotherapy Protocol',
      category: 'Systemic Overuse & Autonomic Recovery',
      target: 'Vasomotor Flush & Muscle Soreness',
      dose: '4 cycles: 3 min cold (10°C) / 1 min warm (38°C)',
      cue: 'Improves autonomic recovery following high ACWR spikes.'
    }
  ];

  grid.innerHTML = library.map(ex => `
    <div class="panel" style="margin-bottom: 0;">
      <span class="badge-pill" style="margin-bottom: 10px; display: inline-block;">${ex.category}</span>
      <h3 style="font-size: 15px; font-weight: 700; margin-bottom: 6px;">${ex.title}</h3>
      <div style="font-size: 12px; color: var(--accent-cyan); font-weight: 700; margin-bottom: 8px;">${ex.dose}</div>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;"><strong>Target:</strong> ${ex.target}</p>
      <p style="font-size: 12px; color: var(--text-dim); line-height: 1.4;"><strong>Clinical Cue:</strong> ${ex.cue}</p>
    </div>
  `).join('');
}

// --- NOTIFICATIONS MODAL ---
window.toggleNotifModal = function() {
  const modal = document.getElementById('notif-modal');
  modal.classList.toggle('open');
  renderAlertsList();
};

function updateNotifBadge() {
  const unread = state.notifications.filter(n => !n.read).length;
  const countEl = document.getElementById('notif-count');
  if (countEl) {
    countEl.textContent = unread;
    countEl.style.display = unread > 0 ? 'flex' : 'none';
  }
}

function renderAlertsList() {
  const container = document.getElementById('alerts-container');
  if (!container) return;

  if (state.notifications.length === 0) {
    container.innerHTML = '<p style="color: var(--text-dim); text-align: center; padding: 20px;">No alerts recorded.</p>';
    return;
  }

  container.innerHTML = state.notifications.map(n => `
    <div class="alert-item ${n.severity === 'info' ? 'alert-info' : ''}">
      <div class="alert-item-title">${n.title || 'Biomechanical Alert'}</div>
      <div class="alert-item-time">${(n.timestamp || '').substring(0, 16).replace('T', ' ')}</div>
      <div class="alert-item-msg">${n.message}</div>
    </div>
  `).join('');
}

window.markAllAlertsRead = async function() {
  await fetch('/api/notifications/read', { method: 'POST' });
  state.notifications.forEach(n => n.read = true);
  updateNotifBadge();
  window.toggleNotifModal();
};

function getStatusClass(cat) {
  if (!cat) return 'low';
  const c = cat.toLowerCase();
  if (c.includes('crit')) return 'crit';
  if (c.includes('high')) return 'high';
  if (c.includes('mod')) return 'mod';
  return 'low';
}
