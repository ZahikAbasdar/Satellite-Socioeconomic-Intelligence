"""
Satellite-Driven Socioeconomic Intelligence
UI Components — Reusable Streamlit elements + CSS theme
"""

import streamlit as st


# ── Master CSS Theme ──────────────────────────────────────────────────────────

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ── Root Variables ── */
:root {
  --bg-primary: #080c14;
  --bg-secondary: #0d1424;
  --bg-card: rgba(255,255,255,0.04);
  --bg-card-hover: rgba(255,255,255,0.07);
  --border: rgba(255,255,255,0.08);
  --border-accent: rgba(99,179,237,0.30);
  --text-primary: #f0f4ff;
  --text-secondary: #8b9dc3;
  --text-muted: #4a5a7a;
  --accent-blue: #63b3ed;
  --accent-cyan: #4fd1c5;
  --accent-green: #68d391;
  --accent-amber: #f6ad55;
  --accent-red: #fc8181;
  --accent-purple: #b794f4;
  --gradient-main: linear-gradient(135deg, #1a2744 0%, #0d1424 50%, #091020 100%);
  --gradient-accent: linear-gradient(135deg, #63b3ed 0%, #4fd1c5 100%);
  --gradient-card: linear-gradient(135deg, rgba(99,179,237,0.08) 0%, rgba(79,209,197,0.04) 100%);
  --shadow-card: 0 4px 24px rgba(0,0,0,0.4), 0 1px 0 rgba(255,255,255,0.05) inset;
  --shadow-glow: 0 0 40px rgba(99,179,237,0.15);
  --radius: 16px;
  --radius-sm: 10px;
  --font-display: 'Syne', sans-serif;
  --font-body: 'DM Sans', sans-serif;
}

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp {
  font-family: var(--font-body);
  background: var(--bg-primary) !important;
  color: var(--text-primary) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: rgba(99,179,237,0.3); border-radius: 3px; }

/* ── Main container ── */
.block-container {
  padding: 2rem 3rem !important;
  max-width: 1400px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0a1020 0%, #080c14 100%) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container {
  padding: 2rem 1.5rem !important;
}

/* ── Typography ── */
h1, h2, h3 { font-family: var(--font-display) !important; }

/* ── Buttons ── */
.stButton > button {
  background: var(--gradient-accent) !important;
  color: #080c14 !important;
  font-family: var(--font-display) !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  padding: 0.75rem 2rem !important;
  transition: all 0.25s ease !important;
  letter-spacing: 0.03em !important;
  box-shadow: 0 4px 20px rgba(99,179,237,0.3) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(99,179,237,0.5) !important;
  filter: brightness(1.1) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
  background: var(--bg-card) !important;
  border: 2px dashed var(--border-accent) !important;
  border-radius: var(--radius) !important;
  padding: 1.5rem !important;
  transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--accent-blue) !important;
}

/* ── Selectbox / Input ── */
.stSelectbox > div > div,
.stNumberInput > div > div {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-card) !important;
  border-radius: var(--radius-sm) !important;
  padding: 4px !important;
  gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 8px !important;
  color: var(--text-secondary) !important;
  font-family: var(--font-body) !important;
  font-weight: 500 !important;
  transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
  background: var(--gradient-accent) !important;
  color: #080c14 !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
  background: var(--gradient-accent) !important;
  border-radius: 4px !important;
}

/* ── Slider ── */
.stSlider > div > div { color: var(--accent-blue) !important; }

/* ── Metric ── */
[data-testid="stMetric"] {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
}

/* ── Expander ── */
.streamlit-expanderHeader {
  background: var(--bg-card) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-display) !important;
}

/* ── Plotly charts ── */
.js-plotly-plot { border-radius: var(--radius) !important; overflow: hidden; }
</style>
"""

COMPONENT_CSS = """
<style>
/* ── KPI Card ── */
.kpi-card {
  background: var(--gradient-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.75rem;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: var(--shadow-card);
}
.kpi-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent 60%, rgba(99,179,237,0.04));
  pointer-events: none;
}
.kpi-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card), var(--shadow-glow);
}
.kpi-label {
  font-family: var(--font-body);
  font-size: 0.80rem;
  font-weight: 500;
  color: var(--text-muted);
  letter-spacing: 0.10em;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}
.kpi-value {
  font-family: var(--font-display);
  font-size: 2.4rem;
  font-weight: 800;
  line-height: 1;
  background: var(--gradient-accent);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.kpi-sub {
  font-family: var(--font-body);
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: 0.4rem;
}
.kpi-icon {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  font-size: 1.8rem;
  opacity: 0.7;
}
.kpi-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.06);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-top: 0.75rem;
}

/* ── Score ring ── */
.score-ring-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}
.score-ring {
  position: relative;
  width: 160px;
  height: 160px;
}
.score-ring svg { transform: rotate(-90deg); }
.score-ring-text {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.score-number {
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 800;
  background: var(--gradient-accent);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.score-label {
  font-size: 0.70rem;
  color: var(--text-muted);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

/* ── Hero section ── */
.hero-wrapper {
  position: relative;
  padding: 4rem 3rem;
  background: linear-gradient(135deg, rgba(99,179,237,0.06) 0%, rgba(79,209,197,0.03) 50%, transparent 100%);
  border: 1px solid var(--border);
  border-radius: 24px;
  margin-bottom: 2.5rem;
  overflow: hidden;
}
.hero-wrapper::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(99,179,237,0.08) 0%, transparent 70%);
  pointer-events: none;
}
.hero-title {
  font-family: var(--font-display);
  font-size: 3.2rem;
  font-weight: 800;
  line-height: 1.05;
  background: linear-gradient(135deg, #f0f4ff 0%, #63b3ed 50%, #4fd1c5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
}
.hero-tagline {
  font-family: var(--font-body);
  font-size: 1.15rem;
  color: var(--text-secondary);
  font-weight: 300;
  max-width: 600px;
  line-height: 1.7;
  margin-bottom: 2rem;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(99,179,237,0.12);
  border: 1px solid rgba(99,179,237,0.25);
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--accent-blue);
  letter-spacing: 0.05em;
  margin-bottom: 1.5rem;
}
.hero-dot {
  width: 8px;
  height: 8px;
  background: var(--accent-cyan);
  border-radius: 50%;
  animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.7); }
}

/* ── Feature card ── */
.feature-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
  height: 100%;
  transition: all 0.25s ease;
  position: relative;
  overflow: hidden;
}
.feature-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-accent);
  opacity: 0;
  transition: opacity 0.25s;
}
.feature-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-accent);
  transform: translateY(-3px);
}
.feature-card:hover::after { opacity: 1; }
.feature-icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
  display: block;
}
.feature-title {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}
.feature-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* ── Section header ── */
.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 1.5rem;
}
.section-header-line {
  flex: 1;
  height: 1px;
  background: var(--border);
}
.section-title {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-secondary);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  white-space: nowrap;
}
.section-dot {
  width: 6px;
  height: 6px;
  background: var(--accent-blue);
  border-radius: 50%;
}

/* ── Status chip ── */
.status-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 14px;
  border-radius: 20px;
  font-size: 0.80rem;
  font-weight: 600;
  letter-spacing: 0.04em;
}
.status-chip-green {
  background: rgba(104,211,145,0.12);
  border: 1px solid rgba(104,211,145,0.25);
  color: #68d391;
}
.status-chip-amber {
  background: rgba(246,173,85,0.12);
  border: 1px solid rgba(246,173,85,0.25);
  color: #f6ad55;
}
.status-chip-red {
  background: rgba(252,129,129,0.12);
  border: 1px solid rgba(252,129,129,0.25);
  color: #fc8181;
}

/* ── Insight box ── */
.insight-box {
  background: linear-gradient(135deg, rgba(99,179,237,0.06) 0%, rgba(79,209,197,0.04) 100%);
  border: 1px solid rgba(99,179,237,0.20);
  border-radius: var(--radius);
  padding: 1.75rem 2rem;
  position: relative;
  overflow: hidden;
}
.insight-box::before {
  content: '"';
  position: absolute;
  top: -20px;
  left: 20px;
  font-size: 8rem;
  color: rgba(99,179,237,0.06);
  font-family: serif;
  line-height: 1;
  pointer-events: none;
}
.insight-text {
  font-family: var(--font-body);
  font-size: 0.92rem;
  color: var(--text-secondary);
  line-height: 1.8;
}

/* ── Divider ── */
.styled-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
  margin: 2rem 0;
}

/* ── Loading overlay ── */
.loading-pulse {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 1rem;
  color: var(--accent-blue);
  font-family: var(--font-body);
  font-size: 0.9rem;
}
.loading-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-blue);
  animation: loading-bounce 1.4s ease-in-out infinite;
}
.loading-dot:nth-child(2) { animation-delay: 0.2s; }
.loading-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes loading-bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1.0); opacity: 1; }
}

/* ── Navbar brand ── */
.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0.5rem 0 2rem;
}
.nav-brand-icon {
  width: 36px;
  height: 36px;
  background: var(--gradient-accent);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}
.nav-brand-name {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.1;
}
.nav-brand-sub {
  font-size: 0.65rem;
  color: var(--text-muted);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.nav-version {
  background: rgba(99,179,237,0.12);
  border: 1px solid rgba(99,179,237,0.20);
  border-radius: 6px;
  padding: 2px 8px;
  font-size: 0.65rem;
  color: var(--accent-blue);
  font-weight: 600;
}
</style>
"""

STAT_GRID_CSS = """
<style>
.stat-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}
</style>
"""


def inject_css():
    """Inject all CSS into Streamlit."""
    st.markdown(DARK_CSS, unsafe_allow_html=True)
    st.markdown(COMPONENT_CSS, unsafe_allow_html=True)
    st.markdown(STAT_GRID_CSS, unsafe_allow_html=True)


def sidebar_brand():
    st.markdown("""
    <div class="nav-brand">
      <div class="nav-brand-icon">🛰️</div>
      <div>
        <div class="nav-brand-name">SatSocio<br>Intelligence</div>
        <div class="nav-version">v2.0</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def kpi_card(label: str, value: str, sub: str = "", icon: str = "", color: str = ""):
    color_style = f"color:{color}; -webkit-text-fill-color:{color};" if color else ""
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value" style="{color_style}">{value}</div>
      <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


def score_ring(score: float, color: str = "#63b3ed"):
    pct = score * 100
    circumference = 2 * 3.14159 * 54
    filled = circumference * score
    gap = circumference - filled
    st.markdown(f"""
    <div class="score-ring-wrapper">
      <div class="score-ring">
        <svg width="160" height="160" viewBox="0 0 160 160">
          <circle cx="80" cy="80" r="54" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="14"/>
          <circle cx="80" cy="80" r="54" fill="none"
            stroke="url(#ringGrad)" stroke-width="14"
            stroke-linecap="round"
            stroke-dasharray="{filled:.1f} {gap:.1f}"/>
          <defs>
            <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#63b3ed"/>
              <stop offset="100%" stop-color="#4fd1c5"/>
            </linearGradient>
          </defs>
        </svg>
        <div class="score-ring-text">
          <div class="score-number">{pct:.0f}</div>
          <div class="score-label">/ 100</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str):
    st.markdown(f"""
    <div class="section-header">
      <div class="section-dot"></div>
      <div class="section-title">{title}</div>
      <div class="section-header-line"></div>
    </div>
    """, unsafe_allow_html=True)


def hero_section():
    st.markdown("""
    <div class="hero-wrapper">
      <div class="hero-badge">
        <div class="hero-dot"></div>
        AI-POWERED · SATELLITE INTELLIGENCE · INDIA + GLOBAL · REAL-TIME
      </div>
      <div class="hero-title">Satellite-Driven<br>Socioeconomic<br>Intelligence</div>
      <div class="hero-tagline">
        Transform raw satellite imagery into actionable socioeconomic insights.
        Our AI engine analyzes land use, nightlights, infrastructure density,
        and spectral signatures to predict development levels with high accuracy.
      </div>
    </div>
    """, unsafe_allow_html=True)


def feature_card(icon: str, title: str, desc: str):
    st.markdown(f"""
    <div class="feature-card">
      <span class="feature-icon">{icon}</span>
      <div class="feature-title">{title}</div>
      <div class="feature-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


def divider():
    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)


def status_chip(text: str, status: str = "green"):
    st.markdown(f'<span class="status-chip status-chip-{status}">{text}</span>',
                unsafe_allow_html=True)


def loading_animation(text: str = "Processing..."):
    st.markdown(f"""
    <div class="loading-pulse">
      <div class="loading-dot"></div>
      <div class="loading-dot"></div>
      <div class="loading-dot"></div>
      <span style="margin-left:4px">{text}</span>
    </div>
    """, unsafe_allow_html=True)


def insight_box(text: str):
    st.markdown(f"""
    <div class="insight-box">
      <div class="insight-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)
