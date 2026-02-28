import os
from pathlib import Path

# ─── Base Paths ───────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# ─── Data File ────────────────────────────────────────────
RAW_DATA_FILE = DATA_RAW_DIR / "German Credit Data.xlsx"
PROCESSED_DATA_FILE = DATA_PROCESSED_DIR / "processed_credit_data.csv"

# ─── Model File ───────────────────────────────────────────
MODEL_FILE = MODELS_DIR / "model_v1.joblib"
SCALER_FILE = MODELS_DIR / "scaler_v1.joblib"

# ─── Model Parameters ─────────────────────────────────────
RANDOM_STATE = 42
TEST_SIZE = 0.2
TARGET_COLUMN = "Risk"

# ─── Feature Columns ──────────────────────────────────────
CATEGORICAL_FEATURES = [
    "Sex",
    "Housing",
    "Saving accounts",
    "Checking account",
    "Purpose"
]

NUMERICAL_FEATURES = [
    "Age",
    "Job",
    "Credit amount",
    "Duration"
]

ALL_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

# ─── API Settings ─────────────────────────────────────────
API_TITLE = "Credit Risk Prediction API"
API_DESCRIPTION = "Production ML API for predicting credit risk"
API_VERSION = "1.0.0"
HOST = "0.0.0.0"
PORT = 8000