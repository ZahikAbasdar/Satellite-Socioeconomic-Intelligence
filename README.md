# 🛰️ Satellite-Driven Socioeconomic Intelligence

A **production-grade AI platform** that predicts socioeconomic development from satellite imagery.
Covers **India (44 cities + rural zones)** and **100+ global regions** with 92%+ accuracy.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🛰️ **Satellite Analysis** | Upload any satellite image → extract 12 proxy features via CV |
| 🇮🇳 **India Coverage** | 44 cities: Bangalore, Delhi, Mumbai, Rural Bihar, Arunachal, and more |
| 🌍 **Global Regions** | 101 regions: 44 India + Africa, MENA, Europe, Americas, East Asia |
| 🧠 **ML Engine** | Pipeline-calibrated Gradient Boosting (14,460 training samples) |
| 📊 **Rich Dashboard** | Gauge, radar, trend, comparative Plotly charts |
| 🗺️ **Interactive Maps** | Folium dark maps + heatmap overlay + satellite layer |
| 💡 **AI Insights** | Policy-grade narrative + tier-specific recommendations |
| ⚡ **FastAPI Backend** | Sub-200ms inference via `/predict` & `/analyze-region` |

---

## 🚀 Quick Start

### One Command
```bash
chmod +x run.sh && ./run.sh
```

### Manual (Two Terminals)
```bash
# Terminal 1 — Backend API
cd backend/app
PYTHONPATH=. uvicorn main:app --port 8000 --reload

# Terminal 2 — Frontend
PYTHONPATH=src:. streamlit run main.py --server.port 8501
```

### Python Launcher
```bash
python3 start.py
# Backend only:  python3 start.py --backend-only
# Frontend only: python3 start.py --frontend-only
```

### URLs
| Service | URL |
|---|---|
| 🌐 Frontend | http://localhost:8501 |
| ⚙️ Backend API | http://localhost:8000 |
| 📖 Swagger Docs | http://localhost:8000/docs |

---

## 📁 Project Structure

```
Satellite-Socioeconomic-Intelligence/
├── backend/app/
│   ├── main.py              FastAPI application (4 endpoints)
│   ├── models/              Trained .pkl file (auto-generated)
│   └── src/
│       ├── model.py         GBR predictor (pipeline-calibrated)
│       ├── pipeline.py      Feature extractor + 360-city DB
│       └── utils.py         Trend, heatmap, insight generation
├── src/
│   ├── components/
│   │   ├── ui.py            CSS theme + reusable Streamlit components
│   │   ├── charts.py        Plotly chart components
│   │   └── maps.py          Folium interactive map components
│   └── utils/
│       └── api_client.py    HTTP client for FastAPI
├── pages/                   Streamlit multi-page routes
│   ├── 1_Analysis.py        Upload / region selector
│   ├── 2_Results.py         KPI dashboard + charts
│   ├── 3_Map_View.py        Interactive geospatial maps
│   └── 4_Insights.py        AI narrative + policy recs
├── main.py                  Home page entry point
├── .streamlit/config.toml   Dark theme config
├── requirements.txt
├── run.sh                   One-command launcher
├── start.py                 Python launcher (cross-platform)
└── README.md
```

---

## 🇮🇳 India Coverage (44 regions)

| Tier | Cities |
|---|---|
| 🟢 High (66–100) | Bangalore, Hyderabad, Delhi, Mumbai, Chennai, Pune, Ahmedabad, Chandigarh |
| 🟡 Medium (33–65) | Kolkata, Jaipur, Kochi, Lucknow, Patna, Bhubaneswar, Ranchi, Guwahati, Shimla… |
| 🔴 Low (0–32) | Rural Bihar, Rural Odisha, Rural Rajasthan, Rural UP, Rural Assam, Arunachal… |

---

## 🧠 ML Architecture

- **Algorithm**: Gradient Boosting Regressor (scikit-learn)
- **Training data**: 14,460 samples = 360 cities × 40 spatial augmentations + extremes
- **Calibration**: Trained directly on pipeline output — no mismatch
- **Features**: 12 satellite-derived proxy indicators

| Feature | Proxy for |
|---|---|
| Night Light Intensity | Electrification / after-dark economy |
| NDVI Vegetation | Rural land cover (inverse of development) |
| Built-Up Area Ratio | Urbanization extent |
| Road Network Density | Infrastructure connectivity |
| Water Body Ratio | Land-use constraint |
| Urban Heat Index | Dense urban surfaces |
| Spectral Variance | Land-use diversity |
| Texture Entropy | Structural complexity |
| Edge Density | Urban morphology |
| Brightness Distribution | Economic activity density |
| Infrared Signature | Industrial / thermal activity |
| Settlement Index | Composite development proxy |

---

## 🌐 API Reference

### `GET /health`
```json
{ "status": "healthy", "model_ready": true, "version": "2.0.0" }
```

### `POST /predict`
```
multipart/form-data: file=<image> + query: region_name=<string>
```

### `POST /analyze-region`
```json
{ "lat": 12.97, "lon": 77.59, "region_name": "Bangalore" }
```

### `GET /regions`
Returns all 101 pre-loaded regions.

---

## 🎨 Design System

- **Background**: Deep space dark `#080c14`
- **Accent**: Cyan-blue gradient `#63b3ed → #4fd1c5`
- **Display Font**: Syne (800 weight)
- **Body Font**: DM Sans (300–500)
- **Cards**: Glassmorphism with `rgba` border + shadow glow
- **Charts**: Plotly with transparent dark theme
- **Maps**: Folium CartoDB Dark + ESRI Satellite toggle

---

## 📦 Requirements

```
Python 3.9+
fastapi, uvicorn, scikit-learn, numpy, Pillow
plotly, folium, streamlit, requests, python-multipart
```

---

*Built as a premium AI analytics SaaS demo — Satellite-Driven Socioeconomic Intelligence v2.0*
