"""
Satellite-Driven Socioeconomic Intelligence
Charts — Plotly visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from typing import List, Dict

# ── Shared Theme ─────────────────────────────────────────────────────────────

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#8b9dc3", size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(color="#8b9dc3"),
        title_font=dict(color="#8b9dc3"),
        showgrid=True,
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(color="#8b9dc3"),
        title_font=dict(color="#8b9dc3"),
        showgrid=True,
    ),
    colorway=["#63b3ed", "#4fd1c5", "#68d391", "#f6ad55", "#fc8181", "#b794f4"],
)

BLUE_GRAD = ["#1a2744", "#63b3ed"]
ACCENT_GRAD = ["#63b3ed", "#4fd1c5", "#68d391"]


def _apply_theme(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family="Syne, sans-serif", size=15, color="#f0f4ff"),
            x=0.01, xanchor="left",
        ),
        **PLOTLY_THEME,
    )
    return fig


# ── Charts ────────────────────────────────────────────────────────────────────

def render_trend_chart(trend: dict, region_name: str = "Region") -> None:
    years = trend["years"]
    scores = [s * 100 for s in trend["scores"]]

    fig = go.Figure()

    # Fill area
    fig.add_trace(go.Scatter(
        x=years, y=scores,
        mode="lines",
        line=dict(color="rgba(99,179,237,0)", width=0),
        fill=None,
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=years, y=scores,
        mode="lines+markers",
        name="Development Score",
        line=dict(color="#63b3ed", width=3, shape="spline", smoothing=1.2),
        marker=dict(
            size=7, color="#63b3ed",
            line=dict(color="#0d1424", width=2),
        ),
        fill="tozeroy",
        fillcolor="rgba(99,179,237,0.08)",
        hovertemplate="<b>%{x}</b><br>Score: %{y:.1f}/100<extra></extra>",
    ))

    fig.update_xaxes(tickmode="array", tickvals=years, tickformat="d")
    fig.update_yaxes(range=[0, 105], ticksuffix="/100")
    _apply_theme(fig, f"📈  Development Trend — {region_name}")

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_feature_bar_chart(features: List[Dict]) -> None:
    top = sorted(features, key=lambda x: x["importance"], reverse=True)[:8]
    names = [f["feature"] for f in top]
    values = [f["value"] for f in top]
    importance = [f["importance"] for f in top]

    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=("Feature Values", "Feature Importance"),
                        horizontal_spacing=0.10)

    colors_val = [f"rgba(99,179,237,{0.4 + 0.6 * v / 100})" for v in values]
    colors_imp = [f"rgba(79,209,197,{0.4 + 0.6 * i / max(importance)})" for i in importance]

    fig.add_trace(go.Bar(
        x=values, y=names, orientation="h",
        marker=dict(color=colors_val,
                    line=dict(color="rgba(99,179,237,0.5)", width=0.5)),
        name="Value", hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=importance, y=names, orientation="h",
        marker=dict(color=colors_imp,
                    line=dict(color="rgba(79,209,197,0.5)", width=0.5)),
        name="Importance", hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ), row=1, col=2)

    fig.update_xaxes(range=[0, 105], ticksuffix="%",
                     gridcolor="rgba(255,255,255,0.05)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")

    _apply_theme(fig, "🔬  Satellite Feature Analysis")
    fig.update_layout(
        height=380,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    for ann in fig.layout.annotations:
        ann.font = dict(family="Syne, sans-serif", size=12, color="#8b9dc3")

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_comparative_chart(comparative: List[Dict]) -> None:
    names = [c["name"] for c in comparative]
    scores = [round(c["score"] * 100, 1) for c in comparative]

    highlight = [
        "#63b3ed" if i == len(comparative) - 1 else "rgba(255,255,255,0.12)"
        for i in range(len(comparative))
    ]

    fig = go.Figure(go.Bar(
        x=names, y=scores,
        marker=dict(
            color=highlight,
            line=dict(color="rgba(99,179,237,0.4)", width=0.5),
            cornerradius=6,
        ),
        hovertemplate="<b>%{x}</b><br>Score: %{y:.1f}/100<extra></extra>",
    ))

    # Add threshold lines
    for y_val, label, col in [
        (33, "Low Threshold", "rgba(252,129,129,0.5)"),
        (66, "High Threshold", "rgba(104,211,145,0.5)"),
    ]:
        fig.add_hline(y=y_val, line=dict(color=col, width=1.5, dash="dot"),
                      annotation_text=label,
                      annotation_font=dict(color=col, size=10))

    fig.update_yaxes(range=[0, 105], ticksuffix="/100")
    _apply_theme(fig, "🌍  Global Benchmark Comparison")
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_radar_chart(features: List[Dict]) -> None:
    top = features[:8]
    names = [f["feature"] for f in top]
    values = [f["value"] for f in top]
    names_closed = names + [names[0]]
    values_closed = values + [values[0]]

    fig = go.Figure(go.Scatterpolar(
        r=values_closed,
        theta=names_closed,
        fill="toself",
        fillcolor="rgba(99,179,237,0.10)",
        line=dict(color="#63b3ed", width=2),
        marker=dict(color="#63b3ed", size=6),
        hovertemplate="%{theta}: %{r:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor="rgba(255,255,255,0.06)",
                linecolor="rgba(255,255,255,0.06)",
                tickfont=dict(color="#8b9dc3", size=9),
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.06)",
                linecolor="rgba(255,255,255,0.08)",
                tickfont=dict(color="#8b9dc3", size=10),
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color="#8b9dc3"),
        margin=dict(l=40, r=40, t=60, b=40),
        title=dict(
            text="🕸️  Feature Radar Profile",
            font=dict(family="Syne, sans-serif", size=15, color="#f0f4ff"),
            x=0.01, xanchor="left",
        ),
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_gauge_chart(score: float, category: str, color: str) -> None:
    pct = score * 100
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pct,
        number=dict(suffix="/100", font=dict(family="Syne", size=36, color="#f0f4ff")),
        delta=dict(reference=55, valueformat=".1f",
                   font=dict(size=14, color="#8b9dc3")),
        gauge=dict(
            axis=dict(
                range=[0, 100], tickwidth=1,
                tickcolor="#4a5a7a", tickfont=dict(color="#8b9dc3"),
            ),
            bar=dict(color=color, thickness=0.5),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            steps=[
                dict(range=[0, 33], color="rgba(252,129,129,0.10)"),
                dict(range=[33, 66], color="rgba(246,173,85,0.10)"),
                dict(range=[66, 100], color="rgba(104,211,145,0.10)"),
            ],
            threshold=dict(
                line=dict(color=color, width=3),
                thickness=0.75,
                value=pct,
            ),
        ),
        title=dict(
            text=f"Development Score — {category}",
            font=dict(family="Syne, sans-serif", size=14, color="#8b9dc3"),
        ),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color="#8b9dc3"),
        height=280,
        margin=dict(l=30, r=30, t=40, b=10),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
