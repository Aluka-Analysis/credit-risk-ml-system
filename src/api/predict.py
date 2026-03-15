# ─── predict.py ───────────────────────────────────────────────
# Handles all prediction logic for the credit risk API
# Loads model once at startup and reuses for all predictions

import joblib
import shap
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
import uuid

# ─── Paths ────────────────────────────────────────────────────
BASE_DIR       = Path(__file__).resolve().parent.parent.parent
MODEL_PATH     = BASE_DIR / "models" / "credit_risk_production_model.pkl"
THRESHOLD_PATH = BASE_DIR / "models" / "optimal_threshold.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

# ─── Feature names ────────────────────────────────────────────
FEATURE_NAMES = [
    "checking account status",
    "Duration in month",
    "Credit history",
    "Purpose",
    "Credit amount",
    "Savings account/bonds",
    "employment",
    "Installment",
    "Other debtors / guarantors",
    "residence",
    "Property",
    "Other installment plans",
    "Housing",
    "existing credits no.",
    "Job",
    "liability responsibles",
    "Telephone"
]
# ─── Numerical columns requiring scaling ──────────────────────
NUMERICAL_COLS = [
    'Duration in month',
    'Credit amount',
    'Installment',
    'residence',
    'existing credits no.',
    'liability responsibles'
]

# ─── Reason mappings ──────────────────────────────────────────
DECLINED_REASONS = {
    "checking account status":
        "Negative or insufficient checking account balance",
    "Duration in month":
        "Extended loan duration relative to risk profile",
    "Credit history":
        "Insufficient credit history or prior defaults",
    "Savings account/bonds":
        "Limited savings or financial reserves",
    "Installment":
        "Current installment obligations relative to income",
    "Credit amount":
        "Loan amount exceeds acceptable risk threshold",
    "Purpose":
        "Loan purpose associated with elevated risk",
    "employment":
        "Employment stability insufficient for loan tenure",
    "Telephone":
        "Unable to verify applicant contact details",
    "Other debtors / guarantors":
        "Guarantor profile associated with elevated risk",
    "Other installment plans":
        "Existing installment plans increase default risk",
    "Housing":
        "Housing situation associated with elevated risk",
    "existing credits no.":
        "Number of existing credits increases risk exposure",
    "Job":
        "Employment type associated with elevated risk",
    "liability responsibles":
        "Number of dependants increases financial burden",
    "residence":
        "Short residence duration associated with elevated risk",
    "Property":
        "Property profile associated with elevated risk"
}

APPROVED_REASONS = {
    "checking account status":
        "Strong positive checking account balance",
    "Duration in month":
        "Loan duration appropriate for risk profile",
    "Credit history":
        "Solid credit history with no prior defaults",
    "Savings account/bonds":
        "Sufficient savings and financial reserves",
    "Installment":
        "Manageable installment obligations relative to income",
    "Credit amount":
        "Loan amount within acceptable risk threshold",
    "Purpose":
        "Loan purpose associated with lower risk",
    "employment":
        "Stable employment supporting loan repayment",
    "Telephone":
        "Applicant has registered contact details "
        "supporting identity verification",
    "Other debtors / guarantors":
        "Guarantor profile associated with lower risk",
    "Other installment plans":
        "Existing installment plans well managed",
    "Housing":
        "Housing situation associated with lower risk",
    "existing credits no.":
        "Manageable number of existing credits",
    "Job":
        "Employment type associated with lower risk",
    "liability responsibles":
        "Low number of dependants reduces financial burden",
    "residence":
        "Stable residence duration associated with lower risk",
    "Property":
        "Property profile associated with lower risk"
}

# ─── Global model and explainer ───────────────────────────────
# Loaded once at startup for performance
_model     = None
_threshold = None
_explainer = None
_scaler    = None


def load_model():
    """
    Load production model and SHAP explainer once at startup.
    Global variables reused for every prediction request.
    """
    global _model, _threshold, _explainer, _scaler
    _model     = joblib.load(MODEL_PATH)
    _threshold = joblib.load(THRESHOLD_PATH)
    _scaler    = joblib.load(SCALER_PATH)
    _explainer = shap.TreeExplainer(_model)
    print("Model, scaler and explainer loaded successfully")
    print(f"Optimal threshold: {_threshold}")
    return _model, _threshold


# ─── Generate prediction ──────────────────────────────────────
def generate_prediction(application_data: dict,
                        model,
                        threshold: float) -> dict:
    """
    Takes raw application data dictionary and returns
    complete credit risk assessment.
    """
    # Convert to dataframe with correct feature names
    input_df = pd.DataFrame([application_data],
                              columns=FEATURE_NAMES)
    
    
    # Scale numerical columns only
    input_scaled = input_df.copy()
    input_scaled[NUMERICAL_COLS] = _scaler.transform(
    input_df[NUMERICAL_COLS]
    )

    # Get probability
    probability = model.predict_proba(input_scaled)[0][1]

    # Make decision
    decision = "DECLINED" if probability >= threshold else "APPROVED"

    # ─── SHAP explanation using global explainer ──────────────
    shap_values = _explainer.shap_values(input_scaled)

    # Get feature contributions
    contributions = pd.DataFrame({
        'Feature':    FEATURE_NAMES,
        'SHAP_Value': shap_values[0]
    })
    contributions = contributions.reindex(
        contributions['SHAP_Value'].abs().sort_values(
            ascending=False).index
    )

    # ─── Generate reasons ─────────────────────────────────────
    if decision == "DECLINED":
        top_features = contributions[
            contributions['SHAP_Value'] > 0].head(3)
        reasons_map  = DECLINED_REASONS
        default_msg  = "{} contributed to elevated risk"
    else:
        top_features = contributions[
            contributions['SHAP_Value'] < 0].head(3)
        reasons_map  = APPROVED_REASONS
        default_msg  = "{} contributed positively to assessment"

    reasons = []
    for _, row in top_features.iterrows():
        feature = row['Feature']
        reason  = reasons_map.get(
            feature, default_msg.format(feature))
        reasons.append(reason)

    if not reasons:
        reasons = ["Assessment based on overall financial profile"]

    # ─── Build response ───────────────────────────────────────
    reference = f"APP-{str(uuid.uuid4())[:8].upper()}"

    return {
        "applicant_reference": reference,
        "decision":            decision,
        "risk_probability":    round(float(probability), 4),
        "risk_percentage":     f"{probability:.1%}",
        "threshold_used":      threshold,
        "top_reasons":         reasons,
        "assessment_date":     datetime.now().strftime("%Y-%m-%d")
    }