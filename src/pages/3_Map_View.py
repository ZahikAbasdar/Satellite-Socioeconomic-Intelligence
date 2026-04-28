"""
Satellite-Driven Socioeconomic Intelligence
Page 3 — Map View
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from components.ui import inject_css, sidebar_brand, section_header, divider
from components.maps import create_map, create_global_overview_map, render_map
from utils.api_client import get_regions, health_check

st.set_page_config(
    page_title="Map View — SatSocio",
    page_icon="🗺️",
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

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem;color:#8b9dc3;font-family:'DM Sans',sans-serif">
      <b style="color:#f0f4ff">Map Controls</b><br><br>
      🗺️ Use layer control (top-right) to switch between Dark and Satellite imagery<br><br>
      🔥 Heatmap shows estimated development intensity<br><br>
      📍 Click markers for detailed popup info<br><br>
      🔍 Use the mini-map (bottom-right) for context
    </div>
    """, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:2rem">
  <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
       background:linear-gradient(135deg,#f0f4ff 0%,#63b3ed 100%);
       -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.5rem">
       🗺️ Map View
  </div>
  <div style="font-size:0.95rem;color:#8b9dc3;font-family:'DM Sans',sans-serif">
    Interactive geospatial visualization with heatmap overlay and development markers.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📍  Analysis Region Map", "🌍  Global Overview Map"])

# ── Tab 1: Analysis region ────────────────────────────────────────────────────
with tab1:
    if "last_result" not in st.session_state:
        st.markdown("""
        <div style="
          text-align:center;padding:4rem 2rem;
          background:rgba(255,255,255,0.02);border:1px dashed rgba(255,255,255,0.07);
          border-radius:16px;color:#4a5a7a;font-family:'DM Sans',sans-serif;
        ">
          <div style="font-size:3rem;margin-bottom:1rem">🗺️</div>
          <div style="font-size:1rem;color:#8b9dc3;margin-bottom:0.5rem;font-weight:500">
            No region analyzed yet
          </div>
          <div style="font-size:0.85rem">
            Run an analysis to see the map for your region.
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.page_link("pages/1_Analysis.py", label="🔬  Go to Analysis →")
    else:
        result = st.session_state["last_result"]
        lat = st.session_state.get("last_lat", 0.0)
        lon = st.session_state.get("last_lon", 0.0)

        col_info, col_ctrl = st.columns([3, 1])
        with col_info:
            st.markdown(f"""
            <div style="
              background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
              border-radius:12px;padding:1rem 1.25rem;margin-bottom:1rem;
              display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap;
            ">
              <div>
                <div style="font-size:0.70rem;color:#4a5a7a;text-transform:uppercase;letter-spacing:0.08em">Region</div>
                <div style="font-size:0.95rem;font-weight:600;color:#f0f4ff">{result['region_name']}</div>
              </div>
              <div>
                <div style="font-size:0.70rem;color:#4a5a7a;text-transform:uppercase;letter-spacing:0.08em">Score</div>
                <div style="font-size:0.95rem;font-weight:700;color:{result['category_color']}">{result['percentage']:.1f}/100</div>
              </div>
              <div>
                <div style="font-size:0.70rem;color:#4a5a7a;text-transform:uppercase;letter-spacing:0.08em">Category</div>
                <div style="font-size:0.95rem;font-weight:600;color:{result['category_color']}">{result['category_icon']} {result['category']}</div>
              </div>
              <div>
                <div style="font-size:0.70rem;color:#4a5a7a;text-transform:uppercase;letter-spacing:0.08em">Coordinates</div>
                <div style="font-size:0.85rem;font-family:monospace;color:#63b3ed">{lat:.4f}°, {lon:.4f}°</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with col_ctrl:
            zoom = st.slider("Map Zoom", min_value=2, max_value=15, value=8, step=1)

        section_header("Interactive Analysis Map")
        map_html = create_map(
            lat=lat, lon=lon,
            score=result["score"],
            category=result["category"],
            region_name=result["region_name"],
            heatmap_data=result.get("heatmap_data", []),
            zoom=zoom,
        )
        render_map(map_html, height=580)

        divider()

        # Legend
        st.markdown("""
        <div style="display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap;
             font-size:0.80rem;font-family:'DM Sans',sans-serif;color:#8b9dc3">
          <b style="color:#f0f4ff">Legend:</b>
          <span><span style="color:#fc8181">●</span> Low Development (&lt;33)</span>
          <span><span style="color:#f6ad55">●</span> Medium Development (33–66)</span>
          <span><span style="color:#68d391">●</span> High Development (&gt;66)</span>
          <span>🔥 Heatmap: development density intensity</span>
        </div>
        """, unsafe_allow_html=True)

# ── Tab 2: Global Overview ────────────────────────────────────────────────────
with tab2:
    section_header("Global Region Overview")

    regions = get_regions()
    if regions:
        # Add cached result score if available
        if "last_result" in st.session_state:
            r = st.session_state["last_result"]
            regions = [reg.copy() for reg in regions]
            for reg in regions:
                # Assign approximate scores based on expected values
                reg["score"] = reg.get("expected", 0.5)

        with st.spinner("Loading global map..."):
            global_html = create_global_overview_map(regions)
        render_map(global_html, height=600)

        divider()

        # Region score table
        section_header("Region Score Table")
        cols = st.columns(4)
        for i, reg in enumerate(sorted(regions, key=lambda x: x.get("expected", 0.5), reverse=True)):
            exp = reg.get("expected", 0.5)
            color = "#68d391" if exp >= 0.66 else "#f6ad55" if exp >= 0.33 else "#fc8181"
            with cols[i % 4]:
                st.markdown(f"""
                <div style="
                  background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                  border-radius:10px;padding:0.75rem;margin-bottom:0.75rem;
                  font-family:'DM Sans',sans-serif;
                ">
                  <div style="font-size:0.75rem;font-weight:600;color:#f0f4ff;margin-bottom:2px">
                    {reg['name']}
                  </div>
                  <div style="font-size:0.80rem;color:{color};font-weight:700">
                    {exp*100:.0f}/100
                  </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Could not load global regions. Backend may be offline.")
