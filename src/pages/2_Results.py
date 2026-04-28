"""
Satellite-Driven Socioeconomic Intelligence
Page 2 — Results Dashboard
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

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
    st.markdown("---")
    st.page_link("main.py", label="🏠  Home")
    st.page_link("pages/1_Analysis.py", label="🔬  Analysis")
    st.page_link("pages/2_Results.py", label="📊  Results Dashboard")
    st.page_link("pages/3_Map_View.py", label="🗺️  Map View")
    st.page_link("pages/4_Insights.py", label="💡  AI Insights")

# ── Guard ─────────────────────────────────────────────────────────────────────
if "last_result" not in st.session_state:
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;font-family:'DM Sans',sans-serif">
      <div style="font-size:4rem;margin-bottom:1.5rem">📊</div>
      <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:700;
           color:#f0f4ff;margin-bottom:0.75rem">No Analysis Results Yet</div>
      <div style="font-size:0.95rem;color:#8b9dc3;margin-bottom:2rem">
        Run an analysis first to view the results dashboard.
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Analysis.py", label="🔬  Go to Analysis →")
    st.stop()

result = st.session_state["last_result"]
score = result["score"]
pct = result["percentage"]
category = result["category"]
color = result["category_color"]
icon = result["category_icon"]
confidence = result["confidence"]
region = result["region_name"]
trend = result["trend"]
features = result["features"]
comparative = result["comparative"]
proc_time = result.get("processing_time_ms", 0)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:2rem;display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:1rem">
  <div>
    <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
         background:linear-gradient(135deg,#f0f4ff 0%,#63b3ed 100%);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.4rem">
         📊 Results Dashboard
    </div>
    <div style="font-size:0.9rem;color:#8b9dc3;font-family:'DM Sans',sans-serif">
      Region: <b style="color:#f0f4ff">{region}</b> &nbsp;·&nbsp;
      Processed in <b style="color:#63b3ed">{proc_time:.0f}ms</b>
    </div>
  </div>
  <div style="
    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
    border-radius:12px;padding:0.75rem 1.25rem;
    font-family:'DM Sans',sans-serif;font-size:0.82rem;color:#8b9dc3;
    display:flex;align-items:center;gap:8px;
  ">
    <span style="font-size:1.1rem">{icon}</span>
    <span style="font-weight:600;color:{color}">{category}</span>
    &nbsp;·&nbsp;
    Confidence: <b style="color:#f0f4ff">{confidence*100:.0f}%</b>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
section_header("Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Development Score", f"{pct:.1f}", f"out of 100 · percentile rank",
             icon="📈", color=color)
with k2:
    kpi_card("Classification", category, f"{icon} Confidence: {confidence*100:.0f}%",
             icon="🏷️")
with k3:
    nightlight = next((f["value"] for f in features if "Night" in f["feature"]), 0)
    kpi_card("Night Light", f"{nightlight:.1f}%",
             "electrification proxy", icon="🌙")
with k4:
    built_up = next((f["value"] for f in features if "Built" in f["feature"]), 0)
    kpi_card("Built-Up Area", f"{built_up:.1f}%",
             "urban land coverage", icon="🏗️")

st.markdown("<br>", unsafe_allow_html=True)

# ── Score Ring + Gauge ────────────────────────────────────────────────────────
col_ring, col_gauge = st.columns([1, 2])
with col_ring:
    st.markdown("""
    <div style="
      background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
      border-radius:16px;padding:1rem;
    ">""", unsafe_allow_html=True)
    section_header("Development Score")
    score_ring(score, color)
    st.markdown(f"""
    <div style="text-align:center;margin-top:0.5rem">
      <div style="font-size:0.80rem;color:#4a5a7a;font-family:'DM Sans',sans-serif">
        Global Rank Tier
      </div>
      <div style="display:inline-flex;align-items:center;gap:6px;
           background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);
           border-radius:20px;padding:4px 14px;margin-top:6px">
        <span style="font-size:1rem">{icon}</span>
        <span style="font-family:'Syne',sans-serif;font-weight:700;color:{color};font-size:0.85rem">
          {category}
        </span>
      </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

with col_gauge:
    st.markdown("""
    <div style="
      background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
      border-radius:16px;padding:1rem;
    ">""", unsafe_allow_html=True)
    section_header("Score Gauge")
    render_gauge_chart(score, category, color)
    st.markdown("</div>", unsafe_allow_html=True)

divider()

# ── Charts ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  Trend", "🔬  Features", "🕸️  Radar", "🌍  Comparison"
])

with tab1:
    render_trend_chart(trend, region)

with tab2:
    render_feature_bar_chart(features)

with tab3:
    render_radar_chart(features)

with tab4:
    render_comparative_chart(comparative)

divider()

# ── Feature Table ─────────────────────────────────────────────────────────────
section_header("Feature Detail Table")

with st.expander("🔍  View All Extracted Features", expanded=False):
    cols = st.columns([3, 2, 2])
    cols[0].markdown("**Feature**")
    cols[1].markdown("**Extracted Value**")
    cols[2].markdown("**Model Importance**")

    for feat in sorted(features, key=lambda x: x["importance"], reverse=True):
        c1, c2, c3 = st.columns([3, 2, 2])
        c1.write(feat["feature"])
        c2.write(f"{feat['value']:.1f}%")
        # Importance bar
        c3.progress(int(feat["importance"]))

divider()

# ── Raw JSON ──────────────────────────────────────────────────────────────────
with st.expander("🛠️  Raw API Response (JSON)", expanded=False):
    import json
    display_result = {k: v for k, v in result.items() if k not in ("heatmap_data",)}
    st.json(display_result)
