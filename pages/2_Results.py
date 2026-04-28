"""
Satellite-Driven Socioeconomic Intelligence
Page 2 — Results Dashboard
"""

import sys
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

import streamlit as st
from components.ui import (
    inject_css, sidebar_brand, section_header, divider,
    kpi_card, score_ring,
)
from components.charts import (
    render_trend_chart, render_feature_bar_chart,
    render_comparative_chart, render_radar_chart, render_gauge_chart,
)
from utils.api_client import health_check

st.set_page_config(
    page_title="Results — SatSocio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

with st.sidebar:
    sidebar_brand()
    st.markdown("---")
    is_healthy = health_check()
    if is_healthy:
        st.markdown("""<div style="display:flex;align-items:center;gap:8px;padding:8px 0">
          <div style="width:8px;height:8px;background:#68d391;border-radius:50%;box-shadow:0 0 8px #68d391;"></div>
          <span style="font-size:0.78rem;color:#68d391;font-weight:600">Backend Online</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="display:flex;align-items:center;gap:8px;padding:8px 0">
          <div style="width:8px;height:8px;background:#fc8181;border-radius:50%;"></div>
          <span style="font-size:0.78rem;color:#fc8181;font-weight:600">Backend Offline</span>
        </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("main.py", label="🏠  Home")
    st.page_link("pages/1_Analysis.py", label="🔬  Analysis")
    st.page_link("pages/2_Results.py", label="📊  Results Dashboard")
    st.page_link("pages/3_Map_View.py", label="🗺️  Map View")
    st.page_link("pages/4_Insights.py", label="💡  AI Insights")
    st.markdown("---")
    st.markdown("""<div style="font-size:0.70rem;color:#4a5a7a;text-align:center;padding:0.5rem 0">
      Satellite Socioeconomic Intelligence v2.0
    </div>""", unsafe_allow_html=True)

# ── Guard: no results ─────────────────────────────────────────────────────────
if "last_result" not in st.session_state:
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;font-family:'DM Sans',sans-serif">
      <div style="font-size:4rem;margin-bottom:1.5rem">📊</div>
      <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:700;
           color:#f0f4ff;margin-bottom:0.75rem">No Analysis Results Yet</div>
      <div style="font-size:0.95rem;color:#8b9dc3;margin-bottom:2rem">
        Run an analysis first to see the full results dashboard.
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Analysis.py", label="🔬  Go to Analysis →")
    st.stop()

# ── Load result ───────────────────────────────────────────────────────────────
result      = st.session_state["last_result"]
score       = result["score"]
pct         = result["percentage"]
category    = result["category"]
color       = result["category_color"]
icon        = result["category_icon"]
confidence  = result["confidence"]
region      = result["region_name"]
trend       = result["trend"]
features    = result["features"]
comparative = result["comparative"]
proc_time   = result.get("processing_time_ms", 0)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:2rem;display:flex;align-items:flex-start;
     justify-content:space-between;flex-wrap:wrap;gap:1rem">
  <div>
    <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
         background:linear-gradient(135deg,#f0f4ff 0%,#63b3ed 100%);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
         margin-bottom:0.4rem">📊 Results Dashboard</div>
    <div style="font-size:0.9rem;color:#8b9dc3;font-family:'DM Sans',sans-serif">
      Region: <b style="color:#f0f4ff">{region}</b>
      &nbsp;·&nbsp; Processed in <b style="color:#63b3ed">{proc_time:.0f}ms</b>
    </div>
  </div>
  <div style="
    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
    border-radius:12px;padding:0.75rem 1.25rem;
    font-family:'DM Sans',sans-serif;font-size:0.82rem;color:#8b9dc3;
    display:flex;align-items:center;gap:10px;
  ">
    <span style="font-size:1.2rem">{icon}</span>
    <span style="font-weight:700;color:{color}">{category}</span>
    &nbsp;·&nbsp; Confidence: <b style="color:#f0f4ff">{confidence*100:.0f}%</b>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
section_header("Key Performance Indicators")
k1, k2, k3, k4 = st.columns(4)

with k1:
    kpi_card("Development Score", f"{pct:.1f}", "out of 100", "📈", color)
with k2:
    kpi_card("Classification", category, f"{icon} {confidence*100:.0f}% confidence", "🏷️")
with k3:
    nightlight = next((f["value"] for f in features if "Night" in f["feature"]), 0)
    kpi_card("Night Light Intensity", f"{nightlight:.1f}%", "electrification proxy", "🌙")
with k4:
    built = next((f["value"] for f in features if "Built" in f["feature"]), 0)
    kpi_card("Built-Up Area", f"{built:.1f}%", "urban land coverage", "🏗️")

st.markdown("<br>", unsafe_allow_html=True)

# ── Score Ring + Gauge ────────────────────────────────────────────────────────
col_ring, col_gauge = st.columns([1, 2])

with col_ring:
    st.markdown("""<div style="background:rgba(255,255,255,0.03);
      border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.25rem;">""",
      unsafe_allow_html=True)
    section_header("Development Score")
    score_ring(score, color)
    st.markdown(f"""
    <div style="text-align:center;margin-top:0.75rem;padding-bottom:0.5rem">
      <div style="
        display:inline-flex;align-items:center;gap:8px;
        background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.09);
        border-radius:20px;padding:5px 16px;
      ">
        <span style="font-size:1.1rem">{icon}</span>
        <span style="font-family:'Syne',sans-serif;font-weight:700;
             color:{color};font-size:0.88rem">{category}</span>
      </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

with col_gauge:
    st.markdown("""<div style="background:rgba(255,255,255,0.03);
      border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.25rem;">""",
      unsafe_allow_html=True)
    section_header("Score Gauge")
    render_gauge_chart(score, category, color)
    st.markdown("</div>", unsafe_allow_html=True)

divider()

# ── Additional KPIs row ───────────────────────────────────────────────────────
section_header("Feature Highlights")
k5, k6, k7, k8 = st.columns(4)

ndvi = next((f["value"] for f in features if "Vegetation" in f["feature"]), 0)
road = next((f["value"] for f in features if "Road" in f["feature"]), 0)
settle = next((f["value"] for f in features if "Settlement" in f["feature"]), 0)
edge = next((f["value"] for f in features if "Edge" in f["feature"]), 0)

with k5:
    kpi_card("NDVI Vegetation", f"{ndvi:.1f}%", "land cover proxy", "🌿")
with k6:
    kpi_card("Road Network", f"{road:.1f}%", "infrastructure density", "🛣️")
with k7:
    kpi_card("Settlement Index", f"{settle:.1f}%", "composite development", "🏘️")
with k8:
    kpi_card("Edge Complexity", f"{edge:.1f}%", "structural richness", "📐")

divider()

# ── Charts Tabs ───────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  Development Trend",
    "🔬  Feature Analysis",
    "🕸️  Radar Profile",
    "🌍  Global Comparison",
])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    render_trend_chart(trend, region)
    st.markdown("""
    <div style="font-size:0.78rem;color:#4a5a7a;font-family:'DM Sans',sans-serif;
         margin-top:0.5rem;padding:0 0.5rem">
      * Historical trend reconstructed from sigmoid growth model anchored to current score.
      Real historical data integration available via API extension.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    render_feature_bar_chart(features)

with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    render_radar_chart(features)

with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    render_comparative_chart(comparative)

divider()

# ── Feature Detail Table ──────────────────────────────────────────────────────
section_header("Feature Detail Table")

with st.expander("🔍  Expand All Extracted Features", expanded=False):
    header_cols = st.columns([3, 2, 2, 4])
    header_cols[0].markdown("<b style='color:#8b9dc3;font-size:0.80rem'>FEATURE</b>",
                             unsafe_allow_html=True)
    header_cols[1].markdown("<b style='color:#8b9dc3;font-size:0.80rem'>VALUE</b>",
                             unsafe_allow_html=True)
    header_cols[2].markdown("<b style='color:#8b9dc3;font-size:0.80rem'>IMPORTANCE</b>",
                             unsafe_allow_html=True)
    header_cols[3].markdown("<b style='color:#8b9dc3;font-size:0.80rem'>DISTRIBUTION</b>",
                             unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.07);margin:8px 0"></div>',
                unsafe_allow_html=True)

    for feat in sorted(features, key=lambda x: x["importance"], reverse=True):
        val = feat["value"]
        imp = feat["importance"]
        val_color = "#68d391" if val > 66 else "#f6ad55" if val > 33 else "#fc8181"

        c1, c2, c3, c4 = st.columns([3, 2, 2, 4])
        c1.markdown(f"<span style='font-size:0.88rem;color:#f0f4ff'>{feat['feature']}</span>",
                    unsafe_allow_html=True)
        c2.markdown(f"<span style='font-size:0.88rem;color:{val_color};font-weight:700'>{val:.1f}%</span>",
                    unsafe_allow_html=True)
        c3.markdown(f"<span style='font-size:0.88rem;color:#63b3ed'>{imp:.1f}%</span>",
                    unsafe_allow_html=True)
        with c4:
            st.progress(int(val))

divider()

# ── Navigation ────────────────────────────────────────────────────────────────
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.page_link("pages/3_Map_View.py", label="🗺️  View on Map →")
with col_b:
    st.page_link("pages/4_Insights.py", label="💡  Read AI Insights →")
with col_c:
    st.page_link("pages/1_Analysis.py", label="🔬  Run New Analysis →")

# ── Raw JSON ──────────────────────────────────────────────────────────────────
with st.expander("🛠️  Raw API Response (JSON)", expanded=False):
    display_result = {k: v for k, v in result.items() if k not in ("heatmap_data",)}
    st.json(display_result)
