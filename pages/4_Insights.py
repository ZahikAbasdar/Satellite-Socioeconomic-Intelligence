"""
Satellite-Driven Socioeconomic Intelligence
Page 4 — AI Insights & Policy Recommendations
"""

import sys
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

import streamlit as st
from components.ui import (
    inject_css, sidebar_brand, section_header, divider,
    kpi_card,
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

# ── Guard ─────────────────────────────────────────────────────────────────────
if "last_result" not in st.session_state:
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;font-family:'DM Sans',sans-serif">
      <div style="font-size:4rem;margin-bottom:1.5rem">💡</div>
      <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:700;
           color:#f0f4ff;margin-bottom:0.75rem">No Insights Generated Yet</div>
      <div style="font-size:0.95rem;color:#8b9dc3;margin-bottom:2rem">
        Run an analysis first to generate AI-powered policy insights.
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Analysis.py", label="🔬  Go to Analysis →")
    st.stop()

# ── Load data ─────────────────────────────────────────────────────────────────
result      = st.session_state["last_result"]
score       = result["score"]
pct         = result["percentage"]
category    = result["category"]
color       = result["category_color"]
icon        = result["category_icon"]
confidence  = result["confidence"]
region      = result["region_name"]
features    = result["features"]
insight_raw = result.get("insight", "No insight available.")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:2rem">
  <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
       background:linear-gradient(135deg,#f0f4ff 0%,#63b3ed 100%);
       -webkit-background-clip:text;-webkit-text-fill-color:transparent;
       margin-bottom:0.4rem">💡 AI Insights</div>
  <div style="font-size:0.9rem;color:#8b9dc3;font-family:'DM Sans',sans-serif">
    Policy-grade AI analysis for <b style="color:#f0f4ff">{region}</b>
    &nbsp;·&nbsp;
    <span style="color:{color};font-weight:600">{icon} {category}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Summary KPIs ──────────────────────────────────────────────────────────────
section_header("Analysis Summary")
k1, k2, k3, k4 = st.columns(4)

top_feat = max(features, key=lambda x: x["importance"])
bottom_feat = min(features, key=lambda x: x["value"])

with k1:
    kpi_card("Development Score", f"{pct:.1f}", "out of 100", "📈", color)
with k2:
    kpi_card("Category", category, f"{icon} classification", "🏷️")
with k3:
    kpi_card("Model Confidence", f"{confidence*100:.0f}%", "prediction certainty", "🎯")
with k4:
    kpi_card("Top Indicator", top_feat["feature"][:18], f"{top_feat['importance']:.0f}% weight", "🔬")

divider()

# ── AI Insight Box ────────────────────────────────────────────────────────────
section_header("AI-Generated Analysis Report")

# Author chip
st.markdown("""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:1.25rem;
     font-family:'DM Sans',sans-serif;">
  <div style="
    width:40px;height:40px;
    background:linear-gradient(135deg,#63b3ed,#4fd1c5);
    border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;
    flex-shrink:0;
  ">🤖</div>
  <div>
    <div style="font-size:0.92rem;font-weight:600;color:#f0f4ff">
      SatSocio Intelligence Engine v2.0
    </div>
    <div style="font-size:0.72rem;color:#4a5a7a">
      Gradient Boosting Model · Satellite Feature Analysis · Policy Report
    </div>
  </div>
  <div style="margin-left:auto;
    background:rgba(104,211,145,0.12);border:1px solid rgba(104,211,145,0.25);
    border-radius:20px;padding:4px 12px;font-size:0.72rem;font-weight:600;color:#68d391;">
    ✅ Analysis Complete
  </div>
</div>
""", unsafe_allow_html=True)

# Render insight as formatted markdown inside a styled container
insight_lines = insight_raw.strip().split("\n")
formatted_html = ""
for line in insight_lines:
    line = line.strip()
    if not line:
        formatted_html += "<br>"
    elif line.startswith("**") and line.endswith("**"):
        formatted_html += f'<div style="font-family:Syne,sans-serif;font-weight:700;color:#f0f4ff;font-size:1rem;margin:0.75rem 0 0.25rem">{line.strip("*")}</div>'
    elif line.startswith("**") and "**" in line[2:]:
        # Bold inline
        import re
        formatted = re.sub(r'\*\*(.*?)\*\*', r'<b style="color:#f0f4ff">\1</b>', line)
        formatted_html += f'<div style="margin-bottom:4px">{formatted}</div>'
    elif line.startswith("- "):
        formatted_html += f'<div style="margin:3px 0;padding-left:1rem;position:relative"><span style="position:absolute;left:0;color:#63b3ed">›</span> {line[2:]}</div>'
    elif line.startswith("*") and line.endswith("*"):
        formatted_html += f'<div style="font-style:italic;color:#4a5a7a;font-size:0.78rem;margin-top:0.5rem">{line.strip("*")}</div>'
    else:
        formatted_html += f'<div style="margin-bottom:6px">{line}</div>'

st.markdown(f"""
<div style="
  background:linear-gradient(135deg,rgba(99,179,237,0.06) 0%,rgba(79,209,197,0.04) 100%);
  border:1px solid rgba(99,179,237,0.20);
  border-left:4px solid #63b3ed;
  border-radius:16px;
  padding:2rem 2.5rem;
  font-family:'DM Sans',sans-serif;
  font-size:0.90rem;
  color:#c8d4e8;
  line-height:1.85;
  position:relative;overflow:hidden;
">
  <div style="
    position:absolute;top:-20px;left:20px;
    font-size:8rem;color:rgba(99,179,237,0.05);
    font-family:serif;line-height:1;pointer-events:none;
  ">"</div>
  <div style="position:relative">{formatted_html}</div>
</div>
""", unsafe_allow_html=True)

divider()

# ── Key Observations ──────────────────────────────────────────────────────────
section_header("Top Feature Observations")

sorted_features = sorted(features, key=lambda x: x["importance"], reverse=True)

for i, feat in enumerate(sorted_features[:6]):
    val = feat["value"]
    imp = feat["importance"]

    if val > 66:
        level, fc, bg, border = "High", "#68d391", "rgba(104,211,145,0.06)", "rgba(104,211,145,0.20)"
        insight = f"Strong indicator of developed conditions — significantly above average threshold."
    elif val > 33:
        level, fc, bg, border = "Moderate", "#f6ad55", "rgba(246,173,85,0.06)", "rgba(246,173,85,0.20)"
        insight = f"Mid-range reading — consistent with transitional or developing status."
    else:
        level, fc, bg, border = "Low", "#fc8181", "rgba(252,129,129,0.06)", "rgba(252,129,129,0.20)"
        insight = f"Below-threshold reading — indicative of infrastructure or development deficits."

    st.markdown(f"""
    <div style="
      background:{bg};border:1px solid {border};border-radius:12px;
      padding:1.25rem 1.5rem;margin-bottom:0.75rem;
      display:grid;grid-template-columns:2rem 1fr auto;gap:1rem;align-items:start;
      font-family:'DM Sans',sans-serif;
    ">
      <div style="
        width:28px;height:28px;min-width:28px;
        background:rgba(255,255,255,0.06);border-radius:50%;
        display:flex;align-items:center;justify-content:center;
        font-weight:800;font-size:0.78rem;color:#8b9dc3;margin-top:2px;
      ">{i+1}</div>
      <div>
        <div style="font-weight:600;color:#f0f4ff;font-size:0.92rem;margin-bottom:6px">
          {feat['feature']}
        </div>
        <div style="height:5px;background:rgba(255,255,255,0.07);border-radius:3px;margin-bottom:6px">
          <div style="width:{val:.0f}%;height:100%;background:{fc};border-radius:3px;opacity:0.75"></div>
        </div>
        <div style="font-size:0.78rem;color:#8b9dc3">{insight}</div>
      </div>
      <div style="text-align:right;white-space:nowrap">
        <div style="
          background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);
          border-radius:8px;padding:4px 10px;font-size:0.72rem;font-weight:700;color:{fc};
          margin-bottom:4px;
        ">{level} · {val:.0f}%</div>
        <div style="font-size:0.68rem;color:#4a5a7a">wt: {imp:.0f}%</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

divider()

# ── Policy Recommendations ────────────────────────────────────────────────────
section_header("Strategic Policy Recommendations")

if score < 0.33:
    tier_label = "Foundational Development"
    tier_desc = "This region is in early-stage development. Focus should be on basic infrastructure, energy access, and human capital."
    recs = [
        ("⚡", "Rural Electrification", "High", "Night-light data confirms severe energy access deficits. Solar mini-grids and national grid extension have highest development multipliers at this stage."),
        ("🛣️", "Rural Road Connectivity", "High", "Infrastructure density metrics indicate critical connectivity gaps. Farm-to-market roads unlock agricultural value chains immediately."),
        ("💧", "WASH Infrastructure", "High", "Clean water and sanitation investment yields 5–10x health and productivity returns in low-development contexts."),
        ("📱", "Mobile Connectivity", "Medium", "Leapfrog traditional infrastructure via mobile towers. Digital financial inclusion accelerates poverty exit by 3–5 years."),
        ("🏥", "Primary Healthcare", "High", "High development returns from maternal and child health investments at this tier."),
        ("🌾", "Agricultural Modernization", "Medium", "Crop diversity and yield improvements support food security and rural income diversification."),
    ]
elif score < 0.66:
    tier_label = "Transitional Development"
    tier_desc = "This region shows solid foundational infrastructure. Now focus on economic diversification, education, and urban planning."
    recs = [
        ("🏫", "Secondary Education", "High", "Investment in secondary and vocational training has highest income multiplier at this development tier."),
        ("🏭", "Light Manufacturing", "High", "Employment elasticity of light manufacturing is 4–6x higher than agriculture at this income level."),
        ("🌆", "Urban Planning", "Medium", "Spectral data shows rapid built-up expansion — proactive zoning prevents slum formation and infrastructure overload."),
        ("💻", "Broadband Infrastructure", "High", "Fiber and 5G investment now enables service-sector emergence within 5 years."),
        ("🏦", "SME Finance", "Medium", "Microfinance and SME lending unlock informal-sector formalization and productivity gains."),
        ("🚇", "Mass Transit", "Medium", "Urban heat and density metrics suggest transportation bottlenecks — bus rapid transit delivers high ROI."),
    ]
else:
    tier_label = "Advanced Development"
    tier_desc = "This is a high-development region. Priorities shift toward sustainability, innovation, and reducing intra-regional inequality."
    recs = [
        ("🌱", "Green Infrastructure", "High", "Urban heat index indicates thermal stress — urban forests, green roofs, and cool corridors are priority investments."),
        ("📊", "Inequality Reduction", "High", "Spectral variance suggests uneven development within the region — targeted investments in lagging sub-areas."),
        ("🔬", "Innovation Ecosystems", "High", "R&D parks, university-industry partnerships, and startup incentives drive sustained high-score growth."),
        ("🤝", "Regional Leadership", "Medium", "Export development capital and expertise to neighboring lower-tier regions — regional stability dividend."),
        ("🏗️", "Infrastructure Renewal", "Medium", "Aging built infrastructure (high built-up ratio) requires renewal investment to avoid depreciation drag."),
        ("♻️", "Circular Economy", "Medium", "Transition to circular material flows reduces environmental externalities that constrain long-term scores."),
    ]

st.markdown(f"""
<div style="
  background:rgba(99,179,237,0.05);border:1px solid rgba(99,179,237,0.15);
  border-radius:12px;padding:1rem 1.5rem;margin-bottom:1.5rem;
  font-family:'DM Sans',sans-serif;
">
  <div style="font-family:'Syne',sans-serif;font-weight:700;color:#f0f4ff;font-size:0.95rem;margin-bottom:4px">
    {tier_label}
  </div>
  <div style="font-size:0.85rem;color:#8b9dc3">{tier_desc}</div>
</div>
""", unsafe_allow_html=True)

cols = st.columns(2)
for i, (rec_icon, rec_title, priority, rec_desc) in enumerate(recs):
    priority_color = "#68d391" if priority == "High" else "#f6ad55"
    priority_bg = "rgba(104,211,145,0.12)" if priority == "High" else "rgba(246,173,85,0.12)"
    with cols[i % 2]:
        st.markdown(f"""
        <div style="
          background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
          border-radius:12px;padding:1.25rem;margin-bottom:0.75rem;
          font-family:'DM Sans',sans-serif;
        ">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
            <span style="font-size:1.25rem">{rec_icon}</span>
            <div style="font-weight:700;color:#f0f4ff;font-size:0.90rem;flex:1">{rec_title}</div>
            <span style="
              background:{priority_bg};border-radius:20px;padding:2px 10px;
              font-size:0.68rem;font-weight:700;color:{priority_color};white-space:nowrap;
            ">{priority} Priority</span>
          </div>
          <div style="font-size:0.80rem;color:#8b9dc3;line-height:1.65">{rec_desc}</div>
        </div>
        """, unsafe_allow_html=True)

divider()

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
  background:rgba(246,173,85,0.05);border:1px solid rgba(246,173,85,0.15);
  border-radius:12px;padding:1rem 1.25rem;
  font-family:'DM Sans',sans-serif;font-size:0.80rem;color:#8b9dc3;
  display:flex;align-items:flex-start;gap:10px;
">
  <span style="font-size:1.1rem;margin-top:1px">⚠️</span>
  <span>
    This report is AI-generated from satellite imagery proxies and should be treated as a
    <b style="color:#f0f4ff">preliminary screening tool</b>.
    Field surveys, administrative data, and domain expert review are required before
    policy decisions. Development scores are relative indicators, not absolute welfare measures.
  </span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.page_link("pages/2_Results.py", label="📊  View Dashboard →")
with col_b:
    st.page_link("pages/3_Map_View.py", label="🗺️  Open Map →")
with col_c:
    st.page_link("pages/1_Analysis.py", label="🔬  New Analysis →")
