"""
Satellite-Driven Socioeconomic Intelligence
API Client — Streamlit ↔ FastAPI Communication
"""

import requests
import streamlit as st
from typing import Optional, BinaryIO
import time

BASE_URL = "http://localhost:8000"
TIMEOUT = 30


def health_check() -> bool:
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def predict_from_image(
    file_bytes: bytes,
    filename: str,
    region_name: str = "Uploaded Region",
) -> Optional[dict]:
    try:
        files = {"file": (filename, file_bytes, "image/jpeg")}
        params = {"region_name": region_name}
        r = requests.post(f"{BASE_URL}/predict", files=files, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
        return None
    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")
        return None


def analyze_region(lat: float, lon: float, region_name: str) -> Optional[dict]:
    try:
        payload = {"lat": lat, "lon": lon, "region_name": region_name}
        r = requests.post(f"{BASE_URL}/analyze-region", json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
        return None
    except Exception as e:
        st.error(f"⚠️ Region analysis failed: {e}")
        return None


def get_regions() -> list:
    try:
        r = requests.get(f"{BASE_URL}/regions", timeout=10)
        r.raise_for_status()
        return r.json().get("regions", [])
    except Exception:
        return []
