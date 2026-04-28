"""
Satellite-Driven Socioeconomic Intelligence
Page 4 — AI Insights
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from components.ui import (
    inject_css, sidebar_brand, section_header, divider,
    insight_box, kpi_card,
)
from utils.api_client import health_check

st.set_page_config(
    page_title="AI Insights — SatSocio",
    page_icon="💡",
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
      <div style="font-size:4rem;margin-bottom:1.5rem">💡</div>
      <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:700;
           color:#f0f4ff;margin-bottom:0.75rem">No Insights Generated Yet</div>
      <div style="font-size:0.95rem;color:#8b9dc3;margin-bottom:2rem">
        Run an analysis first to generate AI-powered insights.
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
features = result["features"]
insight_text = result.get("insight", "No insight available.")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:2rem">
  <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
       background:linear-gradient(135deg,#f0f4ff 0%,#63b3ed 100%);
       -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.4rem">
       💡 AI Insights
  </div>
  <div style="font-size:0.9rem;color:#8b9dc3;font-family:'DM Sans',sans-serif">
    AI-generated policy-grade analysis for <b style="color:#f0f4ff">{region}</b>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Summary KPIs ──────────────────────────────────────────────────────────────
section_header("Analysis Summary")

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Development Score", f"{pct:.1f}", "out of 100", "📈", color)
with k2:
    kpi_card("Category", category, f"{icon} tier", "🏷️")
with k3:
    kpi_card("Confidence", f"{confidence*100:.0f}%", "model certainty", "🎯")
with k4:
    top_feat = max(features, key=lambda x: x["importance"])
    kpi_card("Top Indicator", top_feat["feature"], f"{top_feat['importance']:.0f}% importance", "🔬")

divider()

# ── Main Insight ──────────────────────────────────────────────────────────────
section_header("AI-Generated Analysis")

st.markdown("""
<div style="
  display:flex;align-items:center;gap:10px;margin-bottom:1rem;
  font-family:'DM Sans',sans-serif;
">
  <div style="
    width:36px;height:36px;background:linear-gradient(135deg,#63b3ed,#4fd1c5);
    border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1rem;
  ">🤖</div>
  <div>
    <div style="font-size:0.9rem;font-weight:600;color:#f0f4ff">SatSocio Intelligence Engine</div>
    <div style="font-size:0.72rem;color:#4a5a7a">Gradient Boosting Model · v2.0 · Analysis Report</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Render insight as markdown in styled box
st.markdown(f"""
<div style="
  background:linear-gradient(135deg,rgba(99,179,237,0.06) 0%,rgba(79,209,197,0.04) 100%);
  border:1px solid rgba(99,179,237,0.20);
  border-radius:16px;
  padding:2rem 2.5rem;
  font-family:'DM Sans',sans-serif;
  font-size:0.92rem;
  color:#c8d4e8;
  line-height:1.85;
  position:relative;overflow:hidden;
">
  <div style="
    position:absolute;top:-20px;left:20px;font-size:8rem;
    color:rgba(99,179,237,0.05);font-family:serif;line-height:1;pointer-events:none;
  ">"</div>
  <div style="position:relative;white-space:pre-wrap">{insight_text}</div>
</div>
""", unsafe_allow_html=True)

divider()

# ── Key Observations ──────────────────────────────────────────────────────────
section_header("Key Observations")

sorted_features = sorted(features, key=lambda x: x["importance"], reverse=True)
top5 = sorted_features[:5]

for i, feat in enumerate(top5):
    val = feat["value"]
    imp = feat["importance"]

    if val > 66:
        obs_level = "High"
        obs_color = "#68d391"
        obs_bg = "rgba(104,211,145,0.06)"
        obs_border = "rgba(104,211,145,0.20)"
    elif val > 33:
        obs_level = "Moderate"
        obs_color = "#f6ad55"
        obs_bg = "rgba(246,173,85,0.06)"
        obs_border = "rgba(246,173,85,0.20)"
    else:
        obs_level = "Low"
        obs_color = "#fc8181"
        obs_bg = "rgba(252,129,129,0.06)"
        obs_border = "rgba(252,129,129,0.20)"

    st.markdown(f"""
    <div style="
      background:{obs_bg};border:1px solid {obs_border};
      border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:0.75rem;
      display:flex;align-items:flex-start;gap:1rem;
      font-family:'DM Sans',sans-serif;
    ">
      <div style="
        min-width:32px;height:32px;
        background:rgba(255,255,255,0.06);border-radius:50%;
        display:flex;align-items:center;justify-content:center;
        font-weight:800;font-size:0.85rem;color:#8b9dc3;
      ">{i+1}</div>
      <div style="flex:1">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px">
          <div style="font-weight:600;color:#f0f4ff;font-size:0.92rem">{feat['feature']}</div>
          <div style="
            background:rgba(255,255,255,0.05);border-radius:20px;
            padding:2px 10px;font-size:0.72rem;font-weight:600;color:{obs_color};
          ">{obs_level} · {val:.0f}%</div>
        </div>
        <div style="height:4px;background:rgba(255,255,255,0.06);border-radius:2px;margin:6px 0">
          <div style="width:{val}%;height:100%;background:{obs_color};border-radius:2px;
               opacity:0.7;"></div>
        </div>
        <div style="font-size:0.78rem;color:#8b9dc3">
          Model importance: <b style="color:{obs_color}">{imp:.0f}%</b> of prediction weight
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

divider()

# ── Recommendations ───────────────────────────────────────────────────────────
section_header("Policy Recommendations")

if score < 0.33:
    recs = [
        ("⚡", "Energy Access", "Prioritize rural electrification programs. Night-light data indicates very low energy access, a foundational development constraint."),
        ("🛣️", "Infrastructure", "Road connectivity is a high-leverage investment at this development stage. Focus on rural-urban linkages."),
        ("💧", "Basic Services", "Clean water and sanitation infrastructure should be primary intervention targets."),
        ("📱", "Digital Leapfrog", "Mobile connectivity can leapfrog traditional infrastructure gaps — target telecom towers in dark-light zones."),
    ]
elif score < 0.66:
    recs = [
        ("🏫", "Education", "Secondary and vocational education expansion aligns with the income elasticity of demand at this development stage."),
        ("🏭", "Manufacturing", "Light manufacturing investment shows highest employment multipliers in medium-development regions."),
        ("🌆", "Urban Planning", "Manage urban sprawl proactively — built-up expansion is outpacing infrastructure in this region."),
        ("💻", "Digital Economy", "Broadband infrastructure investment now will enable service-sector diversification within 5 years."),
    ]
else:
    recs = [
        ("🌱", "Green Transition", "High development status enables focus on sustainability — urban heat index indicates overheating risk."),
        ("📊", "Inequality", "Reduce intra-regional development disparities visible in spectral variance across the image."),
        ("🔬", "Innovation", "R&D investment and startup ecosystems are the primary drivers of continued high-score growth."),
        ("🤝", "Regional Aid", "Export development expertise and financing to neighboring lower-development regions."),
    ]

cols = st.columns(2)
for i, (rec_icon, rec_title, rec_desc) in enumerate(recs):
    with cols[i % 2]:
        st.markdown(f"""
        <div style="
          background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
          border-radius:12px;padding:1.25rem;margin-bottom:0.75rem;
          font-family:'DM Sans',sans-serif;
        ">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
            <span style="font-size:1.25rem">{rec_icon}</span>
            <div style="font-weight:700;color:#f0f4ff;font-size:0.92rem">{rec_title}</div>
          </div>
          <div style="font-size:0.82rem;color:#8b9dc3;line-height:1.65">{rec_desc}</div>
        </div>
        """, unsafe_allow_html=True)

divider()

# ── Export Note ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="
  background:rgba(99,179,237,0.05);border:1px solid rgba(99,179,237,0.15);
  border-radius:12px;padding:1rem 1.25rem;
  font-family:'DM Sans',sans-serif;font-size:0.82rem;color:#8b9dc3;
  display:flex;align-items:center;gap:10px;
">
  <span style="font-size:1.1rem">ℹ️</span>
  <span>
    This report is AI-generated based on satellite feature extraction and should be used as a
    preliminary screening tool. Field validation and additional socioeconomic data sources are
    recommended before policy decisions.
  </span>
</div>
""", unsafe_allow_html=True)
