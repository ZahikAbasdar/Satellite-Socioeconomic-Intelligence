"""
Satellite-Driven Socioeconomic Intelligence
ML Model — pipeline-calibrated Gradient Boosting predictor
"""

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pickle
import os
import logging

logger = logging.getLogger(__name__)

FEATURE_NAMES = [
    "nightlight_intensity",
    "ndvi_index",
    "built_up_area_ratio",
    "road_density",
    "water_body_ratio",
    "urban_heat_index",
    "spectral_variance",
    "texture_entropy",
    "edge_density",
    "bright_pixel_ratio",
    "infrared_ratio",
    "settlement_index",
]

CATEGORIES = {
    (0.0,  0.33): ("Low Development",    "#EF4444", "🔴"),
    (0.33, 0.66): ("Medium Development", "#F59E0B", "🟡"),
    (0.66, 1.01): ("High Development",   "#10B981", "🟢"),
}


def classify_score(score: float) -> dict:
    for (lo, hi), (label, color, icon) in CATEGORIES.items():
        if lo <= score < hi:
            return {"label": label, "color": color, "icon": icon}
    return {"label": "High Development", "color": "#10B981", "icon": "🟢"}


def _generate_training_data(n_aug: int = 40) -> tuple:
    """
    Build training data directly from the pipeline's city database so the
    model is perfectly calibrated to real pipeline output.
    Each city generates n_aug augmented samples with tiny noise.
    """
    from src.pipeline import CITY_DATABASE, extract_features_from_region

    rng = np.random.default_rng(42)
    X_rows, y_rows = [], []

    for clat, clon, _radius, cscore in CITY_DATABASE:
        for aug_idx in range(n_aug):
            # Small spatial jitter so we get real pipeline variance
            dlat = rng.normal(0, 0.05)
            dlon = rng.normal(0, 0.05)
            feat = extract_features_from_region(
                clat + dlat, clon + dlon, f"aug_{aug_idx}"
            )
            # Target = city score + tiny label noise
            target = float(np.clip(cscore + rng.normal(0, 0.01), 0.0, 1.0))
            X_rows.append(feat)
            y_rows.append(target)

    # Extra synthetic anchor rows at extreme ends (ensures full [0,1] coverage)
    extremes = [
        ([0.02, 0.96, 0.02, 0.02, 0.05, 0.02, 0.10, 0.15, 0.03, 0.02, 0.12, 0.02], 0.05),
        ([0.05, 0.92, 0.04, 0.03, 0.08, 0.03, 0.14, 0.18, 0.04, 0.04, 0.14, 0.04], 0.10),
        ([0.10, 0.88, 0.08, 0.06, 0.10, 0.05, 0.18, 0.22, 0.06, 0.08, 0.17, 0.07], 0.15),
        ([0.97, 0.05, 0.96, 0.93, 0.02, 0.90, 0.88, 0.93, 0.88, 0.95, 0.44, 0.95], 0.98),
        ([0.95, 0.08, 0.93, 0.90, 0.02, 0.88, 0.85, 0.90, 0.85, 0.93, 0.42, 0.93], 0.96),
    ]
    for feats, score in extremes:
        for _ in range(20):
            noise = rng.normal(0, 0.008, len(feats))
            X_rows.append(np.clip(np.array(feats) + noise, 0, 1).astype(np.float32))
            y_rows.append(float(np.clip(score + rng.normal(0, 0.005), 0, 1)))

    X = np.array(X_rows, dtype=np.float32)
    y = np.array(y_rows, dtype=np.float32)
    logger.info(f"Training data: {X.shape[0]} samples from {len(CITY_DATABASE)} cities × {n_aug} augmentations")
    return X, y


class SocioeconomicPredictor:
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/socio_model.pkl")

    def __init__(self):
        self.regressor = Pipeline([
            ("scaler", StandardScaler()),
            ("gbr", GradientBoostingRegressor(
                n_estimators=400,
                learning_rate=0.04,
                max_depth=6,
                subsample=0.85,
                min_samples_leaf=3,
                random_state=42,
            )),
        ])
        self._trained = False

    def train(self):
        logger.info("Training pipeline-calibrated model …")
        X, y = _generate_training_data(n_aug=40)
        self.regressor.fit(X, y)
        self._trained = True
        self._save()
        logger.info(f"Model trained on {len(X)} samples and saved.")

    def _save(self):
        os.makedirs(os.path.dirname(self.MODEL_PATH), exist_ok=True)
        with open(self.MODEL_PATH, "wb") as f:
            pickle.dump(self.regressor, f)

    def load(self):
        if os.path.exists(self.MODEL_PATH):
            with open(self.MODEL_PATH, "rb") as f:
                self.regressor = pickle.load(f)
            self._trained = True
            logger.info("Model loaded from disk.")
        else:
            self.train()

    def predict(self, features: np.ndarray) -> dict:
        if not self._trained:
            self.load()
        raw = self.regressor.predict(features.reshape(1, -1))[0]
        score = float(np.clip(raw, 0.0, 1.0))
        category = classify_score(score)
        fi = self._feature_importance(features)
        return {
            "score":            round(score, 4),
            "percentage":       round(score * 100, 2),
            "category":         category["label"],
            "category_color":   category["color"],
            "category_icon":    category["icon"],
            "feature_importance": fi,
            "confidence":       round(self._confidence(score), 3),
        }

    def _feature_importance(self, features: np.ndarray) -> dict:
        gbr = self.regressor.named_steps["gbr"]
        imp = gbr.feature_importances_
        return {
            name: {
                "value":      round(float(features[i]), 4),
                "importance": round(float(imp[i]), 4),
            }
            for i, name in enumerate(FEATURE_NAMES)
        }

    def _confidence(self, score: float) -> float:
        dist = min(abs(score - 0.33), abs(score - 0.66), score, 1 - score)
        return min(0.99, 0.68 + dist * 1.8)


_predictor: "SocioeconomicPredictor | None" = None


def get_predictor() -> SocioeconomicPredictor:
    global _predictor
    if _predictor is None:
        _predictor = SocioeconomicPredictor()
        _predictor.load()
    return _predictor
