"""
Satellite-Driven Socioeconomic Intelligence
Page 3 — Interactive Map View
"""

import sys
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

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
    st.markdown("""
    <div style="font-size:0.78rem;color:#8b9dc3;font-family:'DM Sans',sans-serif;line-height:1.8">
      <b style="color:#f0f4ff">Map Tips</b><br><br>
      🗂️ Layer control (top-right) switches between Dark + Satellite<br><br>
      🔥 Heatmap shows development intensity distribution<br><br>
      📍 Click markers for score details<br><br>
      🗺️ Mini-map (bottom-right) for global context<br><br>
      🔍 Scroll to zoom in/out
    </div>
    """, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:2rem">
  <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
       background:linear-gradient(135deg,#f0f4ff 0%,#63b3ed 100%);
       -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.5rem">
       🗺️ Geospatial Map View
  </div>
  <div style="font-size:0.95rem;color:#8b9dc3;font-family:'DM Sans',sans-serif">
    Interactive development heatmaps, regional markers, and satellite imagery overlays.
  </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📍  Analysis Region", "🌍  Global Overview"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Analysis region map
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    if "last_result" not in st.session_state:
        st.markdown("""
        <div style="
          text-align:center;padding:4rem 2rem;
          background:rgba(255,255,255,0.02);border:1px dashed rgba(255,255,255,0.07);
          border-radius:16px;font-family:'DM Sans',sans-serif;margin:1rem 0;
        ">
          <div style="font-size:3rem;margin-bottom:1rem">🗺️</div>
          <div style="font-size:1rem;color:#8b9dc3;margin-bottom:0.5rem;font-weight:500">
            No region analyzed yet
          </div>
          <div style="font-size:0.85rem;color:#4a5a7a">
            Run an analysis to see its geospatial map with heatmap overlay.
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.page_link("pages/1_Analysis.py", label="🔬  Go to Analysis →")
    else:
        result = st.session_state["last_result"]
        lat    = st.session_state.get("last_lat", 0.0)
        lon    = st.session_state.get("last_lon", 0.0)

        # Info strip + zoom control
        col_strip, col_zoom = st.columns([4, 1])
        with col_strip:
            cat_color = result["category_color"]
            st.markdown(f"""
            <div style="
              background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
              border-radius:12px;padding:1rem 1.5rem;margin-bottom:1rem;
              display:flex;align-items:center;gap:2rem;flex-wrap:wrap;
              font-family:'DM Sans',sans-serif;
            ">
              <div>
                <div style="font-size:0.68rem;color:#4a5a7a;text-transform:uppercase;letter-spacing:0.08em">Region</div>
                <div style="font-size:0.95rem;font-weight:600;color:#f0f4ff">{result['region_name']}</div>
              </div>
              <div>
                <div style="font-size:0.68rem;color:#4a5a7a;text-transform:uppercase;letter-spacing:0.08em">Score</div>
                <div style="font-size:0.95rem;font-weight:800;color:{cat_color}">{result['percentage']:.1f}/100</div>
              </div>
              <div>
                <div style="font-size:0.68rem;color:#4a5a7a;text-transform:uppercase;letter-spacing:0.08em">Category</div>
                <div style="font-size:0.90rem;font-weight:600;color:{cat_color}">
                  {result['category_icon']} {result['category']}
                </div>
              </div>
              <div>
                <div style="font-size:0.68rem;color:#4a5a7a;text-transform:uppercase;letter-spacing:0.08em">Coordinates</div>
                <div style="font-size:0.82rem;font-family:monospace;color:#63b3ed">
                  {lat:+.4f}°, {lon:+.4f}°
                </div>
              </div>
              <div>
                <div style="font-size:0.68rem;color:#4a5a7a;text-transform:uppercase;letter-spacing:0.08em">Confidence</div>
                <div style="font-size:0.90rem;font-weight:600;color:#f0f4ff">{result['confidence']*100:.0f}%</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with col_zoom:
            zoom = st.slider("Zoom", min_value=2, max_value=14, value=7, step=1, label_visibility="visible")

        section_header("Interactive Analysis Map")

        with st.spinner("Rendering interactive map..."):
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
        <div style="
          display:flex;align-items:center;gap:2rem;flex-wrap:wrap;
          font-size:0.80rem;font-family:'DM Sans',sans-serif;color:#8b9dc3;
          padding:0 0.25rem;
        ">
          <b style="color:#f0f4ff">Map Legend:</b>
          <span><span style="color:#fc8181;font-size:1rem">●</span>&nbsp; Low Development (&lt;33)</span>
          <span><span style="color:#f6ad55;font-size:1rem">●</span>&nbsp; Medium Development (33–66)</span>
          <span><span style="color:#68d391;font-size:1rem">●</span>&nbsp; High Development (&gt;66)</span>
          <span>🔥 Heatmap: development density proxy</span>
          <span>⭕ Circle: ~50km analysis radius</span>
        </div>
        """, unsafe_allow_html=True)

        divider()
        col_a, col_b = st.columns(2)
        with col_a:
            st.page_link("pages/2_Results.py", label="📊  Back to Results →")
        with col_b:
            st.page_link("pages/4_Insights.py", label="💡  View AI Insights →")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Global overview
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    section_header("Global Development Overview")

    st.markdown("""
    <div style="
      font-size:0.85rem;color:#8b9dc3;font-family:'DM Sans',sans-serif;
      margin-bottom:1rem;
    ">
      All 24 pre-loaded regions shown with expected development scores.
      Click any cluster to expand. Hover markers for details.
    </div>
    """, unsafe_allow_html=True)

    regions = get_regions()
    if not regions:
        st.warning("⚠️ Cannot load regions. Backend may be offline.")
    else:
        # Enrich with scores
        enriched = []
        for r in regions:
            r_copy = dict(r)
            r_copy["score"] = r_copy.get("expected", 0.5)
            enriched.append(r_copy)

        with st.spinner("Loading global map..."):
            global_html = create_global_overview_map(enriched)
        render_map(global_html, height=600)

        divider()

        # Score leaderboard
        section_header("Development Score Leaderboard")

        sorted_regions = sorted(enriched, key=lambda x: x["score"], reverse=True)

        for rank, reg in enumerate(sorted_regions):
            s = reg["score"]
            bar_color = "#68d391" if s >= 0.66 else "#f6ad55" if s >= 0.33 else "#fc8181"
            medal = "🥇" if rank == 0 else "🥈" if rank == 1 else "🥉" if rank == 2 else f"#{rank+1}"

            col_rank, col_name, col_bar, col_score = st.columns([1, 3, 5, 1])
            col_rank.markdown(f"<div style='font-size:0.85rem;color:#8b9dc3;padding:6px 0'>{medal}</div>",
                              unsafe_allow_html=True)
            col_name.markdown(f"<div style='font-size:0.85rem;color:#f0f4ff;padding:6px 0;font-family:DM Sans'>{reg['name']}</div>",
                              unsafe_allow_html=True)
            with col_bar:
                st.markdown(f"""
                <div style="margin:10px 0;background:rgba(255,255,255,0.05);border-radius:4px;height:8px">
                  <div style="width:{s*100:.0f}%;background:{bar_color};border-radius:4px;height:100%;opacity:0.8"></div>
                </div>
                """, unsafe_allow_html=True)
            col_score.markdown(f"<div style='font-size:0.85rem;font-weight:700;color:{bar_color};padding:6px 0'>{s*100:.0f}</div>",
                               unsafe_allow_html=True)
