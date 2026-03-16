# ─── main.py ──────────────────────────────────────────────────
# FastAPI application entry point
# Credit Risk ML System — Phase 6
# Author: Aluka Precious Oluchukwu

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

from src.api.schemas import (LoanApplication,
                              PredictionResponse,
                              HealthResponse,
                              ModelInfoResponse)
from src.api.predict import load_model, generate_prediction
from src.api.adverse_action import generate_adverse_action_notice

# ─── Initialise FastAPI app ───────────────────────────────────
app = FastAPI(
    title="Credit Risk ML System",
    description="""
    A production-grade credit risk assessment API built on 
    the German Credit Dataset.
    
    This API accepts loan application data and returns:
    - Credit risk decision (APPROVED or DECLINED)
    - Risk probability score
    - Plain English explanation of decision
    - Legally compliant adverse action notice
    
    Protected attributes removed from model:
    - Gender and marital status
    - Foreign worker status  
    - Age in years
    
    Built by Aluka Precious Oluchukwu
    Machine Learning Engineer
    """,
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Serve frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def serve_frontend():
    """Serve the bank officer frontend interface."""
    return FileResponse("frontend/index.html")

# ─── CORS Middleware ──────────────────────────────────────────
# Allows frontend to communicate with API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ─── Load model at startup ────────────────────────────────────
pipeline  = None
threshold = None

@app.on_event("startup")
async def startup_event():
    global pipeline, threshold
    pipeline, threshold = load_model()
    print("Model loaded successfully")
    print(f"Optimal threshold: {threshold}")


# ─── Health Check Endpoint ────────────────────────────────────
@app.get("/health",
         response_model=HealthResponse,
         tags=["System"])
async def health_check():
    """
    Confirms the API is running and model is loaded.
    Use this endpoint to verify deployment status.
    """
    return HealthResponse(
        status="healthy",
        model_version="3.0.0",
        threshold=threshold,
        message="Credit Risk ML System is running"
    )


# ─── Model Info Endpoint ──────────────────────────────────────
@app.get("/model-info",
         response_model=ModelInfoResponse,
         tags=["System"])
async def model_info():
    """
    Returns complete information about the deployed model
    including performance metrics and feature details.
    """
    return ModelInfoResponse(
        model_type="Tuned Gradient Boosting Pipeline "
                   "with SMOTE inside cross validation",
        features_used=17,
        protected_attributes_removed=[
            "status n sex — legally protected under "
            "ECOA GDPR and CBN frameworks",
            "foreign worker — legally protected "
            "nationality attribute",
            "Age in years — failed fairness check "
            "DIR below 0.80 threshold"
        ],
        auc_roc=0.7869,
        recall=0.6667,
        precision=0.5479,
        f1_score=0.6015,
        optimal_threshold=threshold,
        training_data="German Credit Dataset — "
                      "1000 applicants 17 features"
    )


# ─── Predict Endpoint ─────────────────────────────────────────
@app.post("/predict",
          response_model=PredictionResponse,
          tags=["Prediction"])
async def predict(application: LoanApplication):
    """
    Accepts a loan application and returns a complete
    credit risk assessment with plain English explanation.
    
    This is the primary endpoint used by bank officers
    to assess credit risk for loan applicants.
    """
    try:
        # Convert application to dictionary
        application_data = {
            "checking account status":
                application.checking_account_status,
            "Duration in month":
                application.duration_in_month,
            "Credit history":
                application.credit_history,
            "Purpose":
                application.purpose,
            "Credit amount":
                application.credit_amount,
            "Savings account/bonds":
                application.savings_account_bonds,
            "employment":
                application.employment,
            "Installment":
                application.installment,
            "Other installment plans":
                application.other_installment_plans,
            "residence":
                application.residence,
            "Property":
                application.property,
            "Housing":
                application.housing,
            "existing credits no.":
                application.existing_credits_no,
            "Job":
                application.job,
            "liability responsibles":
                application.liability_responsibles,
            "Telephone":
                application.telephone,
            "Other debtors / guarantors":
                application.other_debtors_guarantors
        }

        # Generate prediction
        result = generate_prediction(
            application_data, pipeline, threshold)

        # Generate adverse action notice
        notice = generate_adverse_action_notice(
            applicant_reference=result["applicant_reference"],
            decision=result["decision"],
            risk_probability=result["risk_probability"],
            reasons=result["top_reasons"]
        )

        # Print notice to console for audit trail
        print(notice)

        return PredictionResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


# ─── Run application ──────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )