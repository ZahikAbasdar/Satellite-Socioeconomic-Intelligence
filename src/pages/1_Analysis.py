"""
Satellite-Driven Socioeconomic Intelligence
Page 1 — Analysis: Upload & Region Selection
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import streamlit as st
import time
from components.ui import inject_css, sidebar_brand, section_header, divider, loading_animation
from utils.api_client import predict_from_image, analyze_region, get_regions, health_check

st.set_page_config(
    page_title="Analysis — SatSocio",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

with st.sidebar:
    sidebar_brand()
    st.markdown("---")
    is_healthy = health_check()
    if is_healthy:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding:8px 0">
          <div style="width:8px;height:8px;background:#68d391;border-radius:50%;
               box-shadow:0 0 8px #68d391;"></div>
          <span style="font-size:0.78rem;color:#68d391;font-weight:600">Backend Online</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding:8px 0">
          <div style="width:8px;height:8px;background:#fc8181;border-radius:50;"></div>
          <span style="font-size:0.78rem;color:#fc8181;font-weight:600">Backend Offline</span>
        </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("main.py", label="🏠  Home")
    st.page_link("pages/1_Analysis.py", label="🔬  Analysis")
    st.page_link("pages/2_Results.py", label="📊  Results Dashboard")
    st.page_link("pages/3_Map_View.py", label="🗺️  Map View")
    st.page_link("pages/4_Insights.py", label="💡  AI Insights")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:2rem">
  <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
       background:linear-gradient(135deg,#f0f4ff 0%,#63b3ed 100%);
       -webkit-background-clip:text;-webkit-text-fill-color:transparent;
       margin-bottom:0.5rem">🔬 Satellite Analysis</div>
  <div style="font-size:0.95rem;color:#8b9dc3;font-family:'DM Sans',sans-serif">
    Upload a satellite image or select a geographic region to predict socioeconomic development level.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Mode Selector ─────────────────────────────────────────────────────────────
mode = st.radio(
    "Analysis Mode",
    ["📸  Upload Satellite Image", "🌍  Select Global Region", "📍  Custom Coordinates"],
    horizontal=True,
    label_visibility="collapsed",
)

divider()

# ═══════════════════════════════════════════════════════════════════════════════
# MODE 1: Upload Image
# ═══════════════════════════════════════════════════════════════════════════════
if mode == "📸  Upload Satellite Image":
    section_header("Image Upload")

    col_upload, col_info = st.columns([2, 1])

    with col_upload:
        st.markdown("""
        <div style="
          border:2px dashed rgba(99,179,237,0.30);
          border-radius:16px;
          padding:2rem;
          background:rgba(99,179,237,0.04);
          margin-bottom:1rem;
        ">
          <div style="text-align:center;color:#8b9dc3;font-size:0.9rem;margin-bottom:1rem">
            🛰️ Drag & drop your satellite image here<br>
            <span style="font-size:0.75rem;color:#4a5a7a">Supported: JPG, PNG, TIFF • Max 20MB</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Upload satellite image",
            type=["jpg", "jpeg", "png", "tif", "tiff"],
            label_visibility="collapsed",
        )
        region_label = st.text_input(
            "Region Name (optional)",
            value="",
            placeholder="e.g. Mumbai Outskirts, 2024",
        )

    with col_info:
        st.markdown("""
        <div style="
          background:rgba(255,255,255,0.03);
          border:1px solid rgba(255,255,255,0.08);
          border-radius:14px;
          padding:1.5rem;
        ">
          <div style="font-family:'Syne',sans-serif;font-weight:700;margin-bottom:1rem;
               color:#f0f4ff;font-size:0.95rem">📋 What we extract</div>
          <div style="font-size:0.80rem;color:#8b9dc3;line-height:2">
            🌙 Night Light Intensity<br>
            🌿 Vegetation Index (NDVI)<br>
            🏗️ Built-Up Area Ratio<br>
            🛣️ Road Network Density<br>
            💧 Water Body Detection<br>
            🌡️ Urban Heat Index<br>
            📡 Spectral Variance<br>
            🔍 Texture Entropy<br>
            📊 Edge Complexity<br>
            ☀️ Brightness Distribution<br>
            🔴 Infrared Signature<br>
            🏘️ Settlement Index
          </div>
        </div>
        """, unsafe_allow_html=True)

    if uploaded is not None:
        col_prev, col_act = st.columns([1, 1])
        with col_prev:
            st.image(uploaded, caption="📷 Uploaded Satellite Image", use_container_width=True)
        with col_act:
            st.markdown(f"""
            <div style="
              background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
              border-radius:14px;padding:1.5rem;margin-bottom:1rem;
            ">
              <div style="font-size:0.75rem;color:#4a5a7a;text-transform:uppercase;letter-spacing:0.08em">
                File Info
              </div>
              <div style="margin-top:8px;font-size:0.85rem;color:#8b9dc3;line-height:2">
                📄 <b style="color:#f0f4ff">{uploaded.name}</b><br>
                📦 Size: <b style="color:#f0f4ff">{uploaded.size / 1024:.1f} KB</b><br>
                🖼️ Type: <b style="color:#f0f4ff">{uploaded.type}</b>
              </div>
            </div>
            """, unsafe_allow_html=True)

            run = st.button("🚀  Run AI Analysis", use_container_width=True)

        if run:
            label = region_label or uploaded.name
            with st.spinner(""):
                loading_placeholder = st.empty()
                with loading_placeholder:
                    loading_animation("Extracting satellite features...")

                progress = st.progress(0)
                for i in range(1, 6):
                    time.sleep(0.12)
                    progress.progress(i * 20, text=f"Step {i}/5: {'Extracting features' if i==1 else 'Running model' if i==3 else 'Computing insights' if i==4 else 'Finalizing' if i==5 else 'Processing'}")

                result = predict_from_image(uploaded.read(), uploaded.name, label)
                loading_placeholder.empty()
                progress.empty()

            if result:
                st.session_state["last_result"] = result
                st.session_state["last_lat"] = 0.0
                st.session_state["last_lon"] = 0.0
                st.success(f"✅  Analysis complete! Score: **{result['percentage']:.1f}/100** — {result['category']}")
                st.markdown("""
                <div style="margin-top:1rem">
                  <a href="/Results_Dashboard" style="
                    display:inline-flex;align-items:center;gap:6px;
                    background:linear-gradient(135deg,#63b3ed,#4fd1c5);
                    color:#080c14;font-weight:700;font-size:0.9rem;
                    border-radius:10px;padding:0.6rem 1.5rem;text-decoration:none;
                  ">📊 View Full Dashboard →</a>
                </div>
                """, unsafe_allow_html=True)
                st.page_link("pages/2_Results.py", label="📊  Open Results Dashboard →")


# ═══════════════════════════════════════════════════════════════════════════════
# MODE 2: Global Region
# ═══════════════════════════════════════════════════════════════════════════════
elif mode == "🌍  Select Global Region":
    section_header("Global Region Selection")

    regions = get_regions()
    if not regions:
        st.warning("⚠️ Could not load regions. Backend may be offline.")
        st.stop()

    region_names = [r["name"] for r in regions]
    col_sel, col_map = st.columns([1, 1])

    with col_sel:
        selected_name = st.selectbox(
            "Choose a region", region_names,
            help="Select from 24 pre-loaded global cities"
        )
        selected = next(r for r in regions if r["name"] == selected_name)

        st.markdown(f"""
        <div style="
          background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
          border-radius:14px;padding:1.25rem;margin:1rem 0;
        ">
          <div style="font-size:0.75rem;color:#4a5a7a;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px">
            Region Details
          </div>
          <div style="font-size:0.85rem;color:#8b9dc3;line-height:2">
            📍 <b style="color:#f0f4ff">{selected['name']}</b><br>
            🌐 Lat: <b style="color:#63b3ed">{selected['lat']}</b> |
               Lon: <b style="color:#63b3ed">{selected['lon']}</b><br>
            📊 Expected Score: <b style="color:#4fd1c5">{selected.get('expected', 0.5)*100:.0f}/100</b>
          </div>
        </div>
        """, unsafe_allow_html=True)

        run = st.button("🚀  Run AI Analysis", use_container_width=True)

    with col_map:
        import folium
        import streamlit.components.v1 as components

        mini_m = folium.Map(
            location=[selected["lat"], selected["lon"]],
            zoom_start=6,
            tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
            attr="CartoDB",
        )
        folium.Marker(
            [selected["lat"], selected["lon"]],
            tooltip=selected["name"],
            icon=folium.Icon(color="blue", icon="satellite", prefix="fa"),
        ).add_to(mini_m)
        components.html(mini_m._repr_html_(), height=300)

    if run:
        with st.spinner(""):
            loading_animation("Analyzing region via satellite data...")
            progress = st.progress(0)
            for i in range(1, 6):
                time.sleep(0.10)
                progress.progress(i * 20)

            result = analyze_region(selected["lat"], selected["lon"], selected["name"])
            progress.empty()

        if result:
            st.session_state["last_result"] = result
            st.session_state["last_lat"] = selected["lat"]
            st.session_state["last_lon"] = selected["lon"]
            st.success(f"✅  {selected['name']}: Score **{result['percentage']:.1f}/100** — {result['category']}")
            st.page_link("pages/2_Results.py", label="📊  Open Results Dashboard →")


# ═══════════════════════════════════════════════════════════════════════════════
# MODE 3: Custom Coordinates
# ═══════════════════════════════════════════════════════════════════════════════
else:
    section_header("Custom Coordinate Analysis")

    col1, col2, col3 = st.columns(3)
    with col1:
        lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=28.61,
                               step=0.01, format="%.4f")
    with col2:
        lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=77.23,
                               step=0.01, format="%.4f")
    with col3:
        region_name = st.text_input("Region Name", value="Custom Region",
                                     placeholder="e.g. Northern Delhi")

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        run = st.button("🚀  Run AI Analysis", use_container_width=True)

    if run:
        with st.spinner(""):
            loading_animation("Analyzing custom region...")
            progress = st.progress(0)
            for i in range(1, 6):
                time.sleep(0.10)
                progress.progress(i * 20)

            result = analyze_region(lat, lon, region_name)
            progress.empty()

        if result:
            st.session_state["last_result"] = result
            st.session_state["last_lat"] = lat
            st.session_state["last_lon"] = lon
            st.success(f"✅  Score: **{result['percentage']:.1f}/100** — {result['category']}")
            st.page_link("pages/2_Results.py", label="📊  Open Results Dashboard →")

# ── No result yet ─────────────────────────────────────────────────────────────
if "last_result" not in st.session_state:
    divider()
    st.markdown("""
    <div style="
      text-align:center;padding:3rem 2rem;
      background:rgba(255,255,255,0.02);border:1px dashed rgba(255,255,255,0.07);
      border-radius:16px;color:#4a5a7a;font-family:'DM Sans',sans-serif;
    ">
      <div style="font-size:3rem;margin-bottom:1rem">🛰️</div>
      <div style="font-size:1rem;font-weight:500;color:#8b9dc3;margin-bottom:0.5rem">
        No analysis run yet
      </div>
      <div style="font-size:0.85rem">
        Select a mode above and run your first analysis to see results.
      </div>
    </div>
    """, unsafe_allow_html=True)
