# ─── schemas.py ───────────────────────────────────────────────
# Defines input and output data structures for the API
# Pydantic validates all incoming data automatically

from pydantic import BaseModel, Field
from typing import List, Optional


# ─── Input Schema ─────────────────────────────────────────────
class LoanApplication(BaseModel):
    """
    Represents a single loan application submitted
    by a bank officer for credit risk assessment.
    All 17 features after removing protected attributes.
    """
    checking_account_status: float = Field(
        description="Checking account status encoded value")
    duration_in_month: float = Field(
        description="Loan duration in months")
    credit_history: float = Field(
        description="Credit history encoded value")
    purpose: float = Field(
        description="Purpose of loan encoded value")
    credit_amount: float = Field(
        description="Loan amount requested")
    savings_account_bonds: float = Field(
        description="Savings account or bonds encoded value")
    employment: float = Field(
        description="Employment status encoded value")
    installment: float = Field(
        description="Installment rate as percentage of income")
    other_installment_plans: float = Field(
        description="Other installment plans encoded value")
    residence: float = Field(
        description="Years at current residence")
    property: float = Field(
        description="Property type encoded value")
    housing: float = Field(
        description="Housing type encoded value")
    existing_credits_no: float = Field(
        description="Number of existing credits at this bank")
    job: float = Field(
        description="Job type encoded value")
    liability_responsibles: float = Field(
        description="Number of people liable to provide maintenance")
    telephone: float = Field(
        description="Telephone registration encoded value")
    other_debtors_guarantors: float = Field(
        description="Other debtors or guarantors encoded value")

    class Config:
        json_schema_extra = {
            "example": {
                "checking_account_status": 0.0,
                "duration_in_month": 24.0,
                "credit_history": 2.0,
                "purpose": 3.0,
                "credit_amount": 5000.0,
                "savings_account_bonds": 1.0,
                "employment": 2.0,
                "installment": 3.0,
                "other_installment_plans": 0.0,
                "residence": 2.0,
                "property": 1.0,
                "housing": 1.0,
                "existing_credits_no": 1.0,
                "job": 2.0,
                "liability_responsibles": 1.0,
                "telephone": 0.0,
                "other_debtors_guarantors": 0.0
            }
        }


# ─── Output Schema ────────────────────────────────────────────
class PredictionResponse(BaseModel):
    """
    Represents the complete credit risk assessment
    returned to the bank officer after submission.
    """
    applicant_reference: str = Field(
        description="Unique reference for this application")
    decision: str = Field(
        description="APPROVED or DECLINED")
    risk_probability: float = Field(
        description="Probability of default between 0 and 1")
    risk_percentage: str = Field(
        description="Risk probability as percentage string")
    threshold_used: float = Field(
        description="Decision threshold applied")
    top_reasons: List[str] = Field(
        description="Top 3 plain English reasons for decision")
    assessment_date: str = Field(
        description="Date of assessment")


# ─── Health Check Schema ──────────────────────────────────────
class HealthResponse(BaseModel):
    status: str
    model_version: str
    threshold: float
    message: str


# ─── Model Info Schema ────────────────────────────────────────
class ModelInfoResponse(BaseModel):
    model_type: str
    features_used: int
    protected_attributes_removed: List[str]
    auc_roc: float
    recall: float
    precision: float
    f1_score: float
    optimal_threshold: float
    training_data: str