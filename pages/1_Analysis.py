"""
Satellite-Driven Socioeconomic Intelligence
Page 1 — Analysis: Upload & Region Selection
Streamlit multi-page entry — delegates to src/pages/1_Analysis.py logic
"""

import sys
import os

# Add project root and src to path
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

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

# ── Sidebar ───────────────────────────────────────────────────────────────────
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
          <div style="width:8px;height:8px;background:#fc8181;border-radius:50%;"></div>
          <span style="font-size:0.78rem;color:#fc8181;font-weight:600">Backend Offline</span>
        </div>
        <div style="font-size:0.72rem;color:#4a5a7a;margin-top:4px;padding-left:4px">
          Run: uvicorn backend.app.main:app
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("main.py", label="🏠  Home")
    st.page_link("pages/1_Analysis.py", label="🔬  Analysis")
    st.page_link("pages/2_Results.py", label="📊  Results Dashboard")
    st.page_link("pages/3_Map_View.py", label="🗺️  Map View")
    st.page_link("pages/4_Insights.py", label="💡  AI Insights")
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.70rem;color:#4a5a7a;text-align:center;padding:0.5rem 0">
      Satellite-Driven Socioeconomic<br>Intelligence Engine v2.0
    </div>
    """, unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:2rem">
  <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
       background:linear-gradient(135deg,#f0f4ff 0%,#63b3ed 100%);
       -webkit-background-clip:text;-webkit-text-fill-color:transparent;
       margin-bottom:0.5rem">🔬 Satellite Analysis</div>
  <div style="font-size:0.95rem;color:#8b9dc3;font-family:'DM Sans',sans-serif">
    Upload a satellite image or select a geographic region to predict socioeconomic development.
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
# MODE 1: Image Upload
# ═══════════════════════════════════════════════════════════════════════════════
if mode == "📸  Upload Satellite Image":
    section_header("Image Upload")

    col_upload, col_info = st.columns([2, 1])

    with col_upload:
        st.markdown("""
        <div style="
          border:2px dashed rgba(99,179,237,0.30);border-radius:16px;
          padding:2rem;background:rgba(99,179,237,0.04);margin-bottom:1rem;
        ">
          <div style="text-align:center;color:#8b9dc3;font-size:0.9rem;margin-bottom:0.5rem">
            🛰️ Drag & drop your satellite image here
          </div>
          <div style="text-align:center;font-size:0.75rem;color:#4a5a7a">
            Supported: JPG, PNG, TIFF &nbsp;·&nbsp; Max 20 MB
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
            placeholder="e.g. Mumbai Outskirts 2024",
        )

    with col_info:
        st.markdown("""
        <div style="
          background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
          border-radius:14px;padding:1.5rem;
        ">
          <div style="font-family:'Syne',sans-serif;font-weight:700;margin-bottom:1rem;
               color:#f0f4ff;font-size:0.95rem">📋 Extracted Features</div>
          <div style="font-size:0.80rem;color:#8b9dc3;line-height:2.1">
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
            file_size_kb = len(uploaded.getvalue()) / 1024
            st.markdown(f"""
            <div style="
              background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
              border-radius:14px;padding:1.5rem;margin-bottom:1rem;
            ">
              <div style="font-size:0.72rem;color:#4a5a7a;text-transform:uppercase;
                   letter-spacing:0.08em;margin-bottom:8px">File Details</div>
              <div style="font-size:0.85rem;color:#8b9dc3;line-height:2.1">
                📄 <b style="color:#f0f4ff">{uploaded.name}</b><br>
                📦 <b style="color:#63b3ed">{file_size_kb:.1f} KB</b><br>
                🖼️ <b style="color:#f0f4ff">{uploaded.type}</b>
              </div>
            </div>
            """, unsafe_allow_html=True)
            run = st.button("🚀  Run AI Analysis", use_container_width=True, key="run_img")

        if run:
            label = region_label.strip() or uploaded.name
            progress = st.progress(0)
            status_msgs = [
                "🔍 Loading image...",
                "📡 Extracting satellite features...",
                "🧠 Running prediction model...",
                "📊 Computing insights...",
                "✅ Finalizing results...",
            ]
            placeholder = st.empty()
            for i, msg in enumerate(status_msgs):
                with placeholder:
                    loading_animation(msg)
                time.sleep(0.15)
                progress.progress((i + 1) * 20, text=msg)

            image_bytes = uploaded.getvalue()
            result = predict_from_image(image_bytes, uploaded.name, label)
            placeholder.empty()
            progress.empty()

            if result:
                st.session_state["last_result"] = result
                st.session_state["last_lat"] = 0.0
                st.session_state["last_lon"] = 0.0
                cat_color = result["category_color"]
                st.markdown(f"""
                <div style="
                  background:rgba(104,211,145,0.08);border:1px solid rgba(104,211,145,0.25);
                  border-radius:12px;padding:1rem 1.25rem;margin:1rem 0;
                  font-family:'DM Sans',sans-serif;
                ">
                  <div style="font-size:0.72rem;color:#68d391;text-transform:uppercase;
                       letter-spacing:0.08em;margin-bottom:4px">✅ Analysis Complete</div>
                  <div style="font-size:1rem;font-weight:600;color:#f0f4ff">
                    Score: <span style="color:{cat_color}">{result['percentage']:.1f}/100</span>
                    &nbsp;·&nbsp; {result['category_icon']} {result['category']}
                    &nbsp;·&nbsp; Confidence: {result['confidence']*100:.0f}%
                  </div>
                  <div style="font-size:0.78rem;color:#8b9dc3;margin-top:4px">
                    Processed in {result.get('processing_time_ms', 0):.0f}ms
                  </div>
                </div>
                """, unsafe_allow_html=True)
                st.page_link("pages/2_Results.py", label="📊  Open Full Results Dashboard →")

# ═══════════════════════════════════════════════════════════════════════════════
# MODE 2: Global Region
# ═══════════════════════════════════════════════════════════════════════════════
elif mode == "🌍  Select Global Region":
    section_header("Global Region Database")

    regions = get_regions()
    if not regions:
        st.warning("⚠️ Backend offline — cannot load regions. Start the FastAPI server first.")
        st.code("cd backend/app && uvicorn main:app --port 8000", language="bash")
        st.stop()

    region_names = [r["name"] for r in regions]
    col_left, col_right = st.columns([1, 1])

    with col_left:
        selected_name = st.selectbox(
            "Select a global city/region",
            region_names,
            help="24 pre-loaded cities with geographic heuristic analysis",
        )
        selected = next(r for r in regions if r["name"] == selected_name)

        exp_score = selected.get("expected", 0.5)
        exp_color = "#68d391" if exp_score >= 0.66 else "#f6ad55" if exp_score >= 0.33 else "#fc8181"

        st.markdown(f"""
        <div style="
          background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
          border-radius:14px;padding:1.25rem;margin:1rem 0;
          font-family:'DM Sans',sans-serif;
        ">
          <div style="font-size:0.72rem;color:#4a5a7a;text-transform:uppercase;
               letter-spacing:0.08em;margin-bottom:10px">Region Details</div>
          <div style="font-size:0.88rem;color:#8b9dc3;line-height:2.1">
            📍 <b style="color:#f0f4ff;font-size:0.95rem">{selected['name']}</b><br>
            🌐 Latitude: <b style="color:#63b3ed">{selected['lat']:+.4f}°</b><br>
            🌐 Longitude: <b style="color:#63b3ed">{selected['lon']:+.4f}°</b><br>
            📊 Expected Score: <b style="color:{exp_color}">{exp_score*100:.0f}/100</b>
          </div>
        </div>
        """, unsafe_allow_html=True)

        run = st.button("🚀  Run AI Analysis", use_container_width=True, key="run_region")

    with col_right:
        try:
            import folium
            import streamlit.components.v1 as components
            mini_m = folium.Map(
                location=[selected["lat"], selected["lon"]],
                zoom_start=5,
                tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
                attr="CartoDB",
            )
            folium.CircleMarker(
                [selected["lat"], selected["lon"]],
                radius=10, color="#63b3ed", fill=True,
                fill_color="#63b3ed", fill_opacity=0.6,
                tooltip=selected["name"],
            ).add_to(mini_m)
            components.html(mini_m._repr_html_(), height=320)
        except Exception as e:
            st.info(f"Map preview unavailable: {e}")

    if run:
        progress = st.progress(0)
        placeholder = st.empty()
        msgs = ["📡 Fetching geospatial data...", "🧠 Running ML model...",
                "📊 Building insights...", "🗺️ Generating heatmap...", "✅ Done!"]
        for i, msg in enumerate(msgs):
            with placeholder:
                loading_animation(msg)
            time.sleep(0.12)
            progress.progress((i + 1) * 20, text=msg)

        result = analyze_region(selected["lat"], selected["lon"], selected["name"])
        placeholder.empty()
        progress.empty()

        if result:
            st.session_state["last_result"] = result
            st.session_state["last_lat"] = selected["lat"]
            st.session_state["last_lon"] = selected["lon"]
            cat_color = result["category_color"]
            st.markdown(f"""
            <div style="
              background:rgba(104,211,145,0.08);border:1px solid rgba(104,211,145,0.25);
              border-radius:12px;padding:1rem 1.25rem;margin:1rem 0;
              font-family:'DM Sans',sans-serif;
            ">
              <div style="font-size:0.72rem;color:#68d391;text-transform:uppercase;
                   letter-spacing:0.08em;margin-bottom:4px">✅ Analysis Complete</div>
              <div style="font-size:1rem;font-weight:600;color:#f0f4ff">
                {selected['name']}: <span style="color:{cat_color}">{result['percentage']:.1f}/100</span>
                &nbsp;·&nbsp; {result['category_icon']} {result['category']}
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.page_link("pages/2_Results.py", label="📊  Open Results Dashboard →")

# ═══════════════════════════════════════════════════════════════════════════════
# MODE 3: Custom Coordinates
# ═══════════════════════════════════════════════════════════════════════════════
else:
    section_header("Custom Coordinate Analysis")

    st.markdown("""
    <div style="
      background:rgba(246,173,85,0.06);border:1px solid rgba(246,173,85,0.20);
      border-radius:10px;padding:0.75rem 1rem;margin-bottom:1rem;
      font-size:0.80rem;color:#f6ad55;font-family:'DM Sans',sans-serif;
    ">
      ⚠️ Custom coordinates use geographic heuristics for feature estimation.
      For highest accuracy, use real satellite imagery.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0,
                               value=28.6139, step=0.001, format="%.4f",
                               help="Decimal degrees (-90 to 90)")
    with col2:
        lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0,
                               value=77.2090, step=0.001, format="%.4f",
                               help="Decimal degrees (-180 to 180)")
    with col3:
        region_name = st.text_input("Region Name", value="New Delhi, India",
                                     placeholder="Descriptive region name")

    # Live coordinate preview
    try:
        import folium
        import streamlit.components.v1 as components
        mini_m = folium.Map(
            location=[lat, lon], zoom_start=4,
            tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
            attr="CartoDB",
        )
        folium.CircleMarker(
            [lat, lon], radius=10, color="#63b3ed",
            fill=True, fill_color="#63b3ed", fill_opacity=0.6,
            tooltip=f"{region_name} ({lat:.4f}°, {lon:.4f}°)",
        ).add_to(mini_m)
        components.html(mini_m._repr_html_(), height=300)
    except Exception:
        pass

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        run = st.button("🚀  Run AI Analysis", use_container_width=True, key="run_coord")

    if run:
        if not region_name.strip():
            st.error("Please enter a region name.")
        else:
            progress = st.progress(0)
            placeholder = st.empty()
            for i, msg in enumerate(["📍 Locating coordinates...", "🧠 Running model...",
                                      "📊 Building report...", "🗺️ Generating heatmap...", "✅ Done!"]):
                with placeholder:
                    loading_animation(msg)
                time.sleep(0.12)
                progress.progress((i + 1) * 20)
            result = analyze_region(lat, lon, region_name.strip())
            placeholder.empty()
            progress.empty()

            if result:
                st.session_state["last_result"] = result
                st.session_state["last_lat"] = lat
                st.session_state["last_lon"] = lon
                cat_color = result["category_color"]
                st.markdown(f"""
                <div style="
                  background:rgba(104,211,145,0.08);border:1px solid rgba(104,211,145,0.25);
                  border-radius:12px;padding:1rem 1.25rem;margin:1rem 0;
                ">
                  <div style="font-size:0.72rem;color:#68d391;text-transform:uppercase;
                       letter-spacing:0.08em;margin-bottom:4px">✅ Analysis Complete</div>
                  <div style="font-size:1rem;font-weight:600;color:#f0f4ff;font-family:'DM Sans',sans-serif">
                    <span style="color:{cat_color}">{result['percentage']:.1f}/100</span>
                    &nbsp;·&nbsp; {result['category_icon']} {result['category']}
                  </div>
                </div>
                """, unsafe_allow_html=True)
                st.page_link("pages/2_Results.py", label="📊  Open Results Dashboard →")

# ── Empty state ───────────────────────────────────────────────────────────────
if "last_result" not in st.session_state:
    divider()
    st.markdown("""
    <div style="
      text-align:center;padding:2.5rem 2rem;
      background:rgba(255,255,255,0.02);border:1px dashed rgba(255,255,255,0.07);
      border-radius:16px;font-family:'DM Sans',sans-serif;
    ">
      <div style="font-size:2.5rem;margin-bottom:0.75rem">🛰️</div>
      <div style="font-size:0.95rem;font-weight:500;color:#8b9dc3;margin-bottom:0.4rem">
        Ready for analysis
      </div>
      <div style="font-size:0.82rem;color:#4a5a7a">
        Choose a mode above and click <b>Run AI Analysis</b> to begin.
      </div>
    </div>
    """, unsafe_allow_html=True)
