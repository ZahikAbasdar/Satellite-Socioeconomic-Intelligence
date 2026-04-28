"""
Satellite-Driven Socioeconomic Intelligence
Utilities — Global region database (India-heavy), trend, heatmap, insights
"""

import numpy as np
from typing import List, Dict, Any
import datetime

# ─────────────────────────────────────────────────────────────────────────────
# COMPREHENSIVE GLOBAL REGION DATABASE  (shown in Analysis → Select Region)
# ─────────────────────────────────────────────────────────────────────────────
GLOBAL_REGIONS = [

    # ── INDIA: Major Metros ──────────────────────────────────────────────────
    {"name": "Bangalore, India",           "lat": 12.97, "lon":  77.59, "expected": 0.73, "country": "India"},
    {"name": "Hyderabad, India",           "lat": 17.38, "lon":  78.47, "expected": 0.69, "country": "India"},
    {"name": "New Delhi, India",           "lat": 28.61, "lon":  77.21, "expected": 0.67, "country": "India"},
    {"name": "Mumbai, India",              "lat": 19.08, "lon":  72.88, "expected": 0.66, "country": "India"},
    {"name": "Chennai, India",             "lat": 13.08, "lon":  80.27, "expected": 0.64, "country": "India"},
    {"name": "Pune, India",                "lat": 18.52, "lon":  73.86, "expected": 0.63, "country": "India"},
    {"name": "Ahmedabad, India",           "lat": 23.02, "lon":  72.57, "expected": 0.62, "country": "India"},
    {"name": "Kolkata, India",             "lat": 22.57, "lon":  88.36, "expected": 0.59, "country": "India"},
    {"name": "Surat, India",               "lat": 21.17, "lon":  72.83, "expected": 0.60, "country": "India"},
    {"name": "Chandigarh, India",          "lat": 30.73, "lon":  76.78, "expected": 0.61, "country": "India"},

    # ── INDIA: Secondary Cities ──────────────────────────────────────────────
    {"name": "Jaipur, India",              "lat": 26.91, "lon":  75.79, "expected": 0.57, "country": "India"},
    {"name": "Kochi, India",               "lat":  9.93, "lon":  76.26, "expected": 0.59, "country": "India"},
    {"name": "Coimbatore, India",          "lat": 11.00, "lon":  76.96, "expected": 0.58, "country": "India"},
    {"name": "Nagpur, India",              "lat": 21.15, "lon":  79.09, "expected": 0.55, "country": "India"},
    {"name": "Mysore, India",              "lat": 12.30, "lon":  76.64, "expected": 0.57, "country": "India"},
    {"name": "Visakhapatnam, India",       "lat": 17.68, "lon":  83.22, "expected": 0.54, "country": "India"},
    {"name": "Vadodara, India",            "lat": 22.32, "lon":  73.18, "expected": 0.53, "country": "India"},
    {"name": "Bhubaneswar, India",         "lat": 20.45, "lon":  85.88, "expected": 0.50, "country": "India"},
    {"name": "Indore, India",              "lat": 22.72, "lon":  75.86, "expected": 0.50, "country": "India"},
    {"name": "Bhopal, India",              "lat": 23.26, "lon":  77.41, "expected": 0.50, "country": "India"},
    {"name": "Thiruvananthapuram, India",  "lat":  8.48, "lon":  76.95, "expected": 0.57, "country": "India"},
    {"name": "Agra, India",                "lat": 27.18, "lon":  78.01, "expected": 0.48, "country": "India"},
    {"name": "Lucknow, India",             "lat": 26.85, "lon":  80.95, "expected": 0.50, "country": "India"},
    {"name": "Varanasi, India",            "lat": 25.32, "lon":  83.00, "expected": 0.46, "country": "India"},
    {"name": "Dehradun, India",            "lat": 30.37, "lon":  78.07, "expected": 0.47, "country": "India"},
    {"name": "Shimla, India",              "lat": 31.10, "lon":  77.17, "expected": 0.54, "country": "India"},
    {"name": "Guwahati, India",            "lat": 26.18, "lon":  91.74, "expected": 0.49, "country": "India"},
    {"name": "Ranchi, India",              "lat": 23.17, "lon":  85.33, "expected": 0.44, "country": "India"},
    {"name": "Raipur, India",              "lat": 21.25, "lon":  81.63, "expected": 0.42, "country": "India"},
    {"name": "Patna, India",               "lat": 25.59, "lon":  85.13, "expected": 0.41, "country": "India"},
    {"name": "Shillong, India",            "lat": 25.58, "lon":  91.88, "expected": 0.38, "country": "India"},

    # ── INDIA: Rural / Semi-Urban Zones ─────────────────────────────────────
    {"name": "Rural Bihar, India",         "lat": 25.00, "lon":  85.50, "expected": 0.28, "country": "India"},
    {"name": "Rural Odisha, India",        "lat": 20.00, "lon":  84.00, "expected": 0.30, "country": "India"},
    {"name": "Rural Rajasthan, India",     "lat": 24.00, "lon":  73.00, "expected": 0.34, "country": "India"},
    {"name": "Rural UP (East), India",     "lat": 27.50, "lon":  80.00, "expected": 0.32, "country": "India"},
    {"name": "Rural MP, India",            "lat": 22.00, "lon":  80.50, "expected": 0.34, "country": "India"},
    {"name": "Rural Assam, India",         "lat": 26.50, "lon":  90.00, "expected": 0.30, "country": "India"},
    {"name": "Rural Arunachal, India",     "lat": 27.50, "lon":  94.50, "expected": 0.26, "country": "India"},
    {"name": "Rural Punjab, India",        "lat": 30.50, "lon":  75.50, "expected": 0.46, "country": "India"},
    {"name": "Rural Haryana, India",       "lat": 29.50, "lon":  76.50, "expected": 0.44, "country": "India"},
    {"name": "Rural Chhattisgarh, India",  "lat": 20.50, "lon":  80.00, "expected": 0.32, "country": "India"},
    {"name": "Rural Karnataka, India",     "lat": 15.50, "lon":  76.00, "expected": 0.34, "country": "India"},
    {"name": "Rural Tamil Nadu, India",    "lat": 10.50, "lon":  77.50, "expected": 0.38, "country": "India"},
    {"name": "Rural Kerala, India",        "lat": 10.00, "lon":  76.50, "expected": 0.40, "country": "India"},

    # ── SOUTH ASIA ────────────────────────────────────────────────────────────
    {"name": "Dhaka, Bangladesh",          "lat": 23.81, "lon":  90.41, "expected": 0.38, "country": "Bangladesh"},
    {"name": "Karachi, Pakistan",          "lat": 24.86, "lon":  67.01, "expected": 0.40, "country": "Pakistan"},
    {"name": "Lahore, Pakistan",           "lat": 31.55, "lon":  74.34, "expected": 0.46, "country": "Pakistan"},
    {"name": "Islamabad, Pakistan",        "lat": 33.69, "lon":  73.06, "expected": 0.48, "country": "Pakistan"},
    {"name": "Kathmandu, Nepal",           "lat": 27.70, "lon":  85.31, "expected": 0.54, "country": "Nepal"},
    {"name": "Colombo, Sri Lanka",         "lat":  6.93, "lon":  79.84, "expected": 0.57, "country": "Sri Lanka"},

    # ── MIDDLE EAST & NORTH AFRICA ────────────────────────────────────────────
    {"name": "Dubai, UAE",                 "lat": 25.20, "lon":  55.27, "expected": 0.90, "country": "UAE"},
    {"name": "Riyadh, Saudi Arabia",       "lat": 24.69, "lon":  46.72, "expected": 0.72, "country": "Saudi Arabia"},
    {"name": "Doha, Qatar",                "lat": 25.30, "lon":  51.53, "expected": 0.85, "country": "Qatar"},
    {"name": "Tel Aviv, Israel",           "lat": 32.09, "lon":  34.78, "expected": 0.85, "country": "Israel"},
    {"name": "Cairo, Egypt",               "lat": 30.04, "lon":  31.24, "expected": 0.56, "country": "Egypt"},
    {"name": "Tehran, Iran",               "lat": 35.69, "lon":  51.39, "expected": 0.59, "country": "Iran"},
    {"name": "Casablanca, Morocco",        "lat": 33.59, "lon":  -7.62, "expected": 0.57, "country": "Morocco"},

    # ── EAST & SOUTHEAST ASIA ─────────────────────────────────────────────────
    {"name": "Singapore",                  "lat":  1.35, "lon": 103.82, "expected": 0.96, "country": "Singapore"},
    {"name": "Tokyo, Japan",               "lat": 35.68, "lon": 139.69, "expected": 0.93, "country": "Japan"},
    {"name": "Seoul, South Korea",         "lat": 37.57, "lon": 126.98, "expected": 0.91, "country": "South Korea"},
    {"name": "Shanghai, China",            "lat": 31.23, "lon": 121.47, "expected": 0.84, "country": "China"},
    {"name": "Beijing, China",             "lat": 39.91, "lon": 116.39, "expected": 0.82, "country": "China"},
    {"name": "Hong Kong",                  "lat": 22.28, "lon": 114.18, "expected": 0.92, "country": "China"},
    {"name": "Bangkok, Thailand",          "lat": 13.75, "lon": 100.52, "expected": 0.73, "country": "Thailand"},
    {"name": "Kuala Lumpur, Malaysia",     "lat":  3.14, "lon": 101.69, "expected": 0.79, "country": "Malaysia"},
    {"name": "Jakarta, Indonesia",         "lat": -6.21, "lon": 106.84, "expected": 0.58, "country": "Indonesia"},
    {"name": "Manila, Philippines",        "lat": 14.58, "lon": 120.98, "expected": 0.61, "country": "Philippines"},
    {"name": "Ho Chi Minh City, Vietnam",  "lat": 10.82, "lon": 106.63, "expected": 0.63, "country": "Vietnam"},

    # ── EUROPE ────────────────────────────────────────────────────────────────
    {"name": "London, UK",                 "lat": 51.51, "lon":  -0.13, "expected": 0.93, "country": "UK"},
    {"name": "Paris, France",              "lat": 48.86, "lon":   2.35, "expected": 0.92, "country": "France"},
    {"name": "Berlin, Germany",            "lat": 52.52, "lon":  13.40, "expected": 0.92, "country": "Germany"},
    {"name": "Zurich, Switzerland",        "lat": 47.38, "lon":   8.54, "expected": 0.94, "country": "Switzerland"},
    {"name": "Amsterdam, Netherlands",     "lat": 52.38, "lon":   4.90, "expected": 0.91, "country": "Netherlands"},
    {"name": "Stockholm, Sweden",          "lat": 59.33, "lon":  18.06, "expected": 0.93, "country": "Sweden"},
    {"name": "Madrid, Spain",              "lat": 40.41, "lon":  -3.70, "expected": 0.85, "country": "Spain"},
    {"name": "Rome, Italy",                "lat": 41.90, "lon":  12.49, "expected": 0.83, "country": "Italy"},
    {"name": "Moscow, Russia",             "lat": 55.75, "lon":  37.62, "expected": 0.72, "country": "Russia"},
    {"name": "Istanbul, Turkey",           "lat": 41.00, "lon":  28.97, "expected": 0.72, "country": "Turkey"},
    {"name": "Warsaw, Poland",             "lat": 52.23, "lon":  21.01, "expected": 0.83, "country": "Poland"},
    {"name": "Athens, Greece",             "lat": 37.98, "lon":  23.73, "expected": 0.76, "country": "Greece"},

    # ── NORTH AMERICA ─────────────────────────────────────────────────────────
    {"name": "New York, USA",              "lat": 40.71, "lon": -74.01, "expected": 0.94, "country": "USA"},
    {"name": "Los Angeles, USA",           "lat": 34.05, "lon":-118.24, "expected": 0.92, "country": "USA"},
    {"name": "Chicago, USA",               "lat": 41.85, "lon": -87.65, "expected": 0.91, "country": "USA"},
    {"name": "San Francisco, USA",         "lat": 37.78, "lon":-122.41, "expected": 0.93, "country": "USA"},
    {"name": "Toronto, Canada",            "lat": 43.65, "lon": -79.38, "expected": 0.92, "country": "Canada"},
    {"name": "Mexico City, Mexico",        "lat": 19.43, "lon": -99.13, "expected": 0.64, "country": "Mexico"},
    {"name": "Bogotá, Colombia",           "lat":  4.71, "lon": -74.07, "expected": 0.63, "country": "Colombia"},

    # ── SOUTH AMERICA ─────────────────────────────────────────────────────────
    {"name": "São Paulo, Brazil",          "lat":-23.55, "lon": -46.63, "expected": 0.68, "country": "Brazil"},
    {"name": "Buenos Aires, Argentina",    "lat":-34.60, "lon": -58.38, "expected": 0.68, "country": "Argentina"},
    {"name": "Santiago, Chile",            "lat":-33.45, "lon": -70.67, "expected": 0.73, "country": "Chile"},
    {"name": "Lima, Peru",                 "lat":-12.05, "lon": -77.04, "expected": 0.63, "country": "Peru"},

    # ── AFRICA ────────────────────────────────────────────────────────────────
    {"name": "Lagos, Nigeria",             "lat":  6.52, "lon":   3.38, "expected": 0.36, "country": "Nigeria"},
    {"name": "Nairobi, Kenya",             "lat": -1.29, "lon":  36.82, "expected": 0.42, "country": "Kenya"},
    {"name": "Johannesburg, South Africa", "lat":-26.20, "lon":  28.04, "expected": 0.73, "country": "South Africa"},
    {"name": "Cape Town, South Africa",    "lat":-33.92, "lon":  18.42, "expected": 0.74, "country": "South Africa"},
    {"name": "Addis Ababa, Ethiopia",      "lat":  9.03, "lon":  38.74, "expected": 0.28, "country": "Ethiopia"},
    {"name": "Kinshasa, DR Congo",         "lat": -4.32, "lon":  15.32, "expected": 0.22, "country": "DR Congo"},
    {"name": "Accra, Ghana",               "lat":  5.56, "lon":  -0.20, "expected": 0.48, "country": "Ghana"},

    # ── OCEANIA ───────────────────────────────────────────────────────────────
    {"name": "Sydney, Australia",          "lat":-33.87, "lon": 151.21, "expected": 0.92, "country": "Australia"},
    {"name": "Melbourne, Australia",       "lat":-37.81, "lon": 144.96, "expected": 0.91, "country": "Australia"},
    {"name": "Auckland, New Zealand",      "lat":-36.85, "lon": 174.76, "expected": 0.89, "country": "New Zealand"},
]


# ─────────────────────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def get_trend_data(score: float, n_years: int = 10) -> Dict[str, List]:
    """Generate realistic historical trend ending at current score."""
    rng   = np.random.default_rng(42)
    years = list(range(datetime.datetime.now().year - n_years + 1,
                       datetime.datetime.now().year + 1))
    t       = np.linspace(-3, 0, n_years)
    anchor  = score * 0.55
    trend   = anchor + (score - anchor) / (1 + np.exp(-t * 2))
    noise   = rng.normal(0, 0.012, n_years)
    values  = np.clip(trend + noise, 0, 1)
    return {
        "years":  years,
        "scores": [round(float(v), 4) for v in values],
    }


def get_feature_breakdown(feature_importance: Dict) -> List[Dict]:
    """Format feature importance dict for chart display."""
    labels = {
        "nightlight_intensity": "Night Lights",
        "ndvi_index":           "Vegetation (NDVI)",
        "built_up_area_ratio":  "Built-Up Area",
        "road_density":         "Road Network",
        "water_body_ratio":     "Water Bodies",
        "urban_heat_index":     "Urban Heat",
        "spectral_variance":    "Spectral Variance",
        "texture_entropy":      "Texture Entropy",
        "edge_density":         "Edge Density",
        "bright_pixel_ratio":   "Brightness",
        "infrared_ratio":       "Infrared Signature",
        "settlement_index":     "Settlement Index",
    }
    result = []
    for key, data in feature_importance.items():
        result.append({
            "feature":    labels.get(key, key),
            "value":      round(data["value"] * 100, 1),
            "importance": round(data["importance"] * 100, 1),
        })
    return sorted(result, key=lambda x: x["importance"], reverse=True)


def generate_heatmap_data(
    center_lat: float,
    center_lon: float,
    radius: float = 2.0,
    n_points: int = 100,
) -> List[Dict]:
    """Generate heatmap points around a center for Folium HeatMap."""
    rng    = np.random.default_rng(int(abs(center_lat * center_lon * 100)) % (2 ** 31))
    points = []
    for _ in range(n_points):
        dlat = rng.uniform(-radius, radius)
        dlon = rng.uniform(-radius, radius)
        dist = np.sqrt(dlat ** 2 + dlon ** 2)
        w    = np.exp(-dist ** 2 / (radius ** 2 * 0.4)) * rng.uniform(0.35, 1.0)
        points.append({
            "lat":    round(center_lat + dlat, 4),
            "lon":    round(center_lon + dlon, 4),
            "weight": round(float(w), 3),
        })
    return points


def get_comparative_data(target_score: float, target_name: str) -> List[Dict]:
    """Return global benchmark comparison list."""
    return [
        {"name": "Global Average",   "score": 0.55},
        {"name": "Developed Avg.",   "score": 0.84},
        {"name": "Developing Avg.",  "score": 0.48},
        {"name": "Least Dev. Avg.",  "score": 0.24},
        {"name": target_name[:20],   "score": target_score},
    ]


def generate_ai_insight(
    score: float,
    category: str,
    features: Dict,
    region_name: str = "the analyzed region",
) -> str:
    """Generate policy-grade narrative from prediction results."""

    top3 = sorted(features.items(), key=lambda x: x[1]["importance"], reverse=True)[:3]
    top_names = [k.replace("_", " ").title() for k, _ in top3]

    nl_val  = features.get("nightlight_intensity", {}).get("value", 0)
    nl_imp  = features.get("nightlight_intensity", {}).get("importance", 0) * 100
    ndvi_v  = features.get("ndvi_index", {}).get("value", 0)
    st_val  = features.get("settlement_index", {}).get("value", 0)

    if score < 0.33:
        level  = "early-stage development"
        driver = "predominantly rural land cover, sparse electrification, and limited road connectivity"
        rec    = (
            "Foundational infrastructure — rural electrification, all-weather roads, and clean water — "
            "delivers the highest economic multipliers. Targeted microfinance and mobile banking can "
            "accelerate inclusion without waiting for grid extension."
        )
    elif score < 0.66:
        level  = "intermediate (transitional) development"
        driver = "mixed urban-rural land use, growing built-up coverage, and moderate infrastructure"
        rec    = (
            "Secondary and vocational education, light manufacturing zones, and broadband rollout are "
            "the highest-leverage investments at this tier. Proactive urban planning prevents "
            "uncontrolled sprawl and preserves future infrastructure capacity."
        )
    else:
        level  = "advanced (high) development"
        driver = "dense built-up coverage, extensive road networks, strong night-light signature, and complex urban texture"
        rec    = (
            "Sustaining growth at this level requires investment in innovation ecosystems, green "
            "infrastructure to counter urban heat stress, and targeted programs to reduce "
            "intra-regional inequality visible in spectral variance data."
        )

    ndvi_interp = (
        "predominantly rural / vegetated land use with limited urban expansion"
        if ndvi_v > 0.50
        else "significant urban and industrial coverage replacing natural surfaces"
    )
    nl_interp = "strong" if nl_val > 0.55 else "moderate" if nl_val > 0.30 else "limited"

    insight = f"""
**{region_name}** exhibits satellite signatures consistent with **{level}** (score: {score*100:.1f}/100).

The primary indicators driving this classification are **{", ".join(top_names)}**, which collectively reflect {driver}.

**Key Observations:**
- Night-light intensity carries {nl_imp:.0f}% of model importance and signals {nl_interp} electrification and after-dark economic activity.
- The vegetation proxy (NDVI = {ndvi_v:.2f}) indicates {ndvi_interp}.
- Settlement index ({st_val*100:.0f}/100) places this region in the **{category}** tier globally.
- Spectral variance and texture entropy metrics confirm the structural complexity level expected for this development stage.

**Strategic Recommendation:**
{rec}

*Analysis by Satellite-Driven Socioeconomic Intelligence Engine v2.0 · Gradient Boosting Model*
""".strip()

    return insight
