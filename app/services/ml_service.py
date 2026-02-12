import json
import os
import joblib
from app.core.config import settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # app/
MODELS_DIR = os.path.join(BASE_DIR, "models")

def _metadata_path() -> str:
    return os.path.join(MODELS_DIR, "metadata.json")

def get_active_version() -> str:
    # priority: env MODEL_VERSION; fallback metadata.json
    if settings.MODEL_VERSION:
        return settings.MODEL_VERSION

    try:
        with open(_metadata_path(), "r", encoding="utf-8") as f:
            meta = json.load(f)
        return meta.get("current_version", "v1")
    except FileNotFoundError:
        return "v1"

def _load_artifacts(version: str):
    model_path = os.path.join(MODELS_DIR, version, "classifier.joblib")
    vec_path = os.path.join(MODELS_DIR, version, "vectorizer.joblib")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    return model, vectorizer

_MODEL = None
_VEC = None
_VERSION = None

def ensure_loaded():
    global _MODEL, _VEC, _VERSION
    v = get_active_version()
    if _MODEL is None or _VEC is None or _VERSION != v:
        _MODEL, _VEC = _load_artifacts(v)
        _VERSION = v

def predict_category(text: str) -> str:
    ensure_loaded()
    X = _VEC.transform([text])
    return str(_MODEL.predict(X)[0])

def model_info() -> dict:
    ensure_loaded()
    return {"model_version": _VERSION}
