"""
Satellite-Driven Socioeconomic Intelligence
Maps — Folium interactive map components
"""

import folium
from folium.plugins import HeatMap, MarkerCluster, MiniMap
import streamlit as st
import streamlit.components.v1 as components
from typing import List, Dict, Optional


CATEGORY_COLORS = {
    "High Development":   "#68d391",
    "Medium Development": "#f6ad55",
    "Low Development":    "#fc8181",
}


def score_to_color(score: float) -> str:
    if score >= 0.66:
        return "#68d391"
    elif score >= 0.33:
        return "#f6ad55"
    return "#fc8181"


def create_map(
    lat: float,
    lon: float,
    score: float,
    category: str,
    region_name: str,
    heatmap_data: List[Dict],
    zoom: int = 8,
) -> str:
    """Build Folium map and return HTML string."""

    m = folium.Map(
        location=[lat, lon],
        zoom_start=zoom,
        tiles=None,
        prefer_canvas=True,
    )

    # ── Tile layers ──────────────────────────────────────────────────────────
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr="CartoDB",
        name="Dark Base",
        max_zoom=19,
    ).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite",
        max_zoom=19,
    ).add_to(m)

    # ── Heatmap ──────────────────────────────────────────────────────────────
    heat_points = [
        [pt["lat"], pt["lon"], pt["weight"]]
        for pt in heatmap_data
    ]
    HeatMap(
        heat_points,
        name="Development Heatmap",
        min_opacity=0.3,
        radius=30,
        blur=25,
        gradient={0.2: "#1a2744", 0.4: "#f6ad55", 0.7: "#68d391", 1.0: "#63b3ed"},
    ).add_to(m)

    # ── Main marker ──────────────────────────────────────────────────────────
    color = score_to_color(score)
    icon_html = f"""
    <div style="
      background:{color};
      width:44px; height:44px;
      border-radius:50%;
      display:flex; align-items:center; justify-content:center;
      font-size:18px;
      box-shadow:0 0 20px {color}80, 0 0 40px {color}30;
      border:3px solid rgba(255,255,255,0.9);
    ">🛰️</div>
    """
    popup_html = f"""
    <div style="
      font-family:'DM Sans',sans-serif;
      background:#0d1424;
      color:#f0f4ff;
      border-radius:12px;
      padding:16px 20px;
      min-width:240px;
      border:1px solid rgba(255,255,255,0.1);
      box-shadow:0 8px 32px rgba(0,0,0,0.5);
    ">
      <div style="font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:#4a5a7a;margin-bottom:6px">
        ANALYSIS TARGET
      </div>
      <div style="font-size:1.1rem;font-weight:700;margin-bottom:12px">{region_name}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
        <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:8px">
          <div style="font-size:0.65rem;color:#8b9dc3;text-transform:uppercase">Score</div>
          <div style="font-size:1.3rem;font-weight:800;color:{color}">{score*100:.1f}</div>
        </div>
        <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:8px">
          <div style="font-size:0.65rem;color:#8b9dc3;text-transform:uppercase">Class</div>
          <div style="font-size:0.75rem;font-weight:600;color:{color}">{category}</div>
        </div>
      </div>
      <div style="margin-top:8px;font-size:0.72rem;color:#4a5a7a">
        📍 {lat:.4f}°, {lon:.4f}°
      </div>
    </div>
    """
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=280),
        tooltip=f"📍 {region_name} — Score: {score*100:.1f}",
        icon=folium.DivIcon(html=icon_html, icon_size=(44, 44), icon_anchor=(22, 22)),
    ).add_to(m)

    # ── Radius circle ────────────────────────────────────────────────────────
    folium.Circle(
        location=[lat, lon],
        radius=50000,
        color=color,
        weight=2,
        opacity=0.5,
        fill=True,
        fill_color=color,
        fill_opacity=0.05,
        tooltip="Analysis radius (~50 km)",
    ).add_to(m)

    # ── MiniMap ──────────────────────────────────────────────────────────────
    MiniMap(
        tile_layer="CartoDB dark_matter",
        toggle_display=True,
        position="bottomright",
        width=120,
        height=80,
        zoom_level_fixed=2,
    ).add_to(m)

    folium.LayerControl(position="topright", collapsed=False).add_to(m)

    return m._repr_html_()


def create_global_overview_map(regions_data: List[Dict]) -> str:
    """Build a global overview map with all analyzed regions."""
    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr="CartoDB",
        prefer_canvas=True,
    )

    cluster = MarkerCluster(name="Regions").add_to(m)

    for region in regions_data:
        score = region.get("score", region.get("expected", 0.5))
        color = score_to_color(score)
        icon_html = f"""
        <div style="
          background:{color}22;
          border:2px solid {color};
          width:28px; height:28px;
          border-radius:50%;
          display:flex; align-items:center; justify-content:center;
          font-size:11px;
          color:{color};
          font-weight:bold;
        ">{int(score*100)}</div>
        """
        popup_html = f"""
        <div style="font-family:'DM Sans',sans-serif;background:#0d1424;color:#f0f4ff;
             border-radius:10px;padding:12px;min-width:180px;border:1px solid rgba(255,255,255,0.1)">
          <b style="font-size:0.95rem">{region['name']}</b>
          <div style="color:{color};font-size:0.85rem;margin-top:4px">
            Score: {score*100:.0f}/100
          </div>
        </div>
        """
        folium.Marker(
            location=[region["lat"], region["lon"]],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"{region['name']}: {score*100:.0f}",
            icon=folium.DivIcon(html=icon_html, icon_size=(28, 28), icon_anchor=(14, 14)),
        ).add_to(cluster)

    return m._repr_html_()


def render_map(html: str, height: int = 500) -> None:
    """Render Folium map in Streamlit."""
    components.html(html, height=height, scrolling=False)
