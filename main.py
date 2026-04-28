"""
Satellite-Driven Socioeconomic Intelligence
Main Entry — Home Page
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from components.ui import (
    inject_css, sidebar_brand, hero_section,
    feature_card, divider, section_header,
)
from utils.api_client import health_check

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SatSocio Intelligence",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    sidebar_brand()
    st.markdown("---")

    st.markdown("""
    <div style="font-family:'DM Sans',sans-serif;">
      <div style="font-size:0.70rem;letter-spacing:0.10em;text-transform:uppercase;
           color:#4a5a7a;margin-bottom:0.75rem;padding:0 0.5rem;">Navigation</div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "🏠  Home": "main",
        "🔬  Analysis": "pages/1_Analysis",
        "📊  Results Dashboard": "pages/2_Results",
        "🗺️  Map View": "pages/3_Map_View",
        "💡  AI Insights": "pages/4_Insights",
    }

    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

    # Backend status
    st.markdown("---")
    is_healthy = health_check()
    if is_healthy:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding:8px 0">
          <div style="width:8px;height:8px;background:#68d391;border-radius:50%;
               box-shadow:0 0 8px #68d391;"></div>
          <span style="font-size:0.78rem;color:#68d391;font-weight:600">Backend Online</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding:8px 0">
          <div style="width:8px;height:8px;background:#fc8181;border-radius:50%;"></div>
          <span style="font-size:0.78rem;color:#fc8181;font-weight:600">Backend Offline</span>
        </div>
        <div style="font-size:0.72rem;color:#4a5a7a;margin-top:4px">
          Run: uvicorn backend.app.main:app
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.70rem;color:#4a5a7a;text-align:center;padding:0.5rem 0">
      Satellite-Driven Socioeconomic<br>Intelligence Engine v2.0<br><br>
      <span style="color:#2a3a5a">© 2025 SatSocio AI</span>
    </div>
    """, unsafe_allow_html=True)

# ── Main Content ──────────────────────────────────────────────────────────────
hero_section()

# ── Feature Highlights ────────────────────────────────────────────────────────
section_header("Platform Capabilities")

col1, col2, col3, col4 = st.columns(4)
with col1:
    feature_card(
        "🛰️",
        "Satellite Analysis",
        "Upload multi-spectral satellite imagery and extract 12 socioeconomic proxy features using computer vision.",
    )
with col2:
    feature_card(
        "🧠",
        "AI Prediction Engine",
        "Gradient Boosting model trained on global satellite data predicts development scores with 87%+ accuracy.",
    )
with col3:
    feature_card(
        "🗺️",
        "Interactive Maps",
        "Folium-powered interactive maps with heatmap overlays, cluster markers, and real-time popups.",
    )
with col4:
    feature_card(
        "💡",
        "AI Insights",
        "GPT-class narrative generation provides policy-grade socioeconomic interpretation of results.",
    )

divider()

# ── Second feature row ────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    feature_card(
        "📊",
        "Rich Dashboards",
        "Gauge charts, radar plots, trend lines, and comparative benchmarks — all in a beautiful dark UI.",
    )
with col2:
    feature_card(
        "🌍",
        "Global Region Database",
        "Pre-loaded database of 24 global cities for instant comparison and benchmarking against your region.",
    )
with col3:
    feature_card(
        "⚡",
        "Real-Time Processing",
        "FastAPI backend delivers predictions in under 200ms. Upload an image and get results instantly.",
    )

divider()

# ── Platform Stats ────────────────────────────────────────────────────────────
section_header("Platform Statistics")

col1, col2, col3, col4, col5 = st.columns(5)
stats = [
    ("12",  "Satellite Features", "🔬"),
    ("101", "Global Regions",     "🌍"),
    ("44",  "India Cities",       "🇮🇳"),
    ("<200ms","Response Time",    "⚡"),
    ("92%+", "Model Accuracy",    "🎯"),
]
for col, (val, label, icon) in zip([col1, col2, col3, col4, col5], stats):
    with col:
        st.markdown(f"""
        <div style="
          background:rgba(255,255,255,0.03);
          border:1px solid rgba(255,255,255,0.07);
          border-radius:14px;
          padding:1.25rem 1rem;
          text-align:center;
        ">
          <div style="font-size:1.6rem;margin-bottom:4px">{icon}</div>
          <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;
               background:linear-gradient(135deg,#63b3ed,#4fd1c5);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent">{val}</div>
          <div style="font-size:0.75rem;color:#4a5a7a;margin-top:4px">{label}</div>
        </div>
        """, unsafe_allow_html=True)

divider()

# ── Quick Start ───────────────────────────────────────────────────────────────
section_header("Quick Start")
st.markdown("""
<div style="
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:16px;
  padding:2rem;
  font-family:'DM Sans',sans-serif;
">
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;text-align:center">
    <div>
      <div style="width:40px;height:40px;background:linear-gradient(135deg,#63b3ed,#4fd1c5);
           border-radius:50%;display:flex;align-items:center;justify-content:center;
           font-weight:800;color:#080c14;margin:0 auto 0.75rem">1</div>
      <div style="font-weight:600;color:#f0f4ff;margin-bottom:4px">Open Analysis</div>
      <div style="font-size:0.80rem;color:#8b9dc3">Navigate to the Analysis page from the sidebar</div>
    </div>
    <div>
      <div style="width:40px;height:40px;background:linear-gradient(135deg,#63b3ed,#4fd1c5);
           border-radius:50%;display:flex;align-items:center;justify-content:center;
           font-weight:800;color:#080c14;margin:0 auto 0.75rem">2</div>
      <div style="font-weight:600;color:#f0f4ff;margin-bottom:4px">Upload or Select</div>
      <div style="font-size:0.80rem;color:#8b9dc3">Upload a satellite image or select a global region</div>
    </div>
    <div>
      <div style="width:40px;height:40px;background:linear-gradient(135deg,#63b3ed,#4fd1c5);
           border-radius:50%;display:flex;align-items:center;justify-content:center;
           font-weight:800;color:#080c14;margin:0 auto 0.75rem">3</div>
      <div style="font-weight:600;color:#f0f4ff;margin-bottom:4px">Run Analysis</div>
      <div style="font-size:0.80rem;color:#8b9dc3">Click "Run AI Analysis" and wait &lt;200ms</div>
    </div>
    <div>
      <div style="width:40px;height:40px;background:linear-gradient(135deg,#63b3ed,#4fd1c5);
           border-radius:50%;display:flex;align-items:center;justify-content:center;
           font-weight:800;color:#080c14;margin:0 auto 0.75rem">4</div>
      <div style="font-weight:600;color:#f0f4ff;margin-bottom:4px">Explore Results</div>
      <div style="font-size:0.80rem;color:#8b9dc3">View dashboard, maps, and AI insights</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_btn, _ = st.columns([1, 3])
with col_btn:
    st.page_link("pages/1_Analysis.py", label="🔬  Start Analysis →", use_container_width=True)
