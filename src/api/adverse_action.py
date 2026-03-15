# ─── adverse_action.py ────────────────────────────────────────
# Generates formal adverse action notices for every decision
# Required by ECOA, GDPR, and CBN Consumer Protection Framework

from datetime import datetime


def generate_adverse_action_notice(
        applicant_reference: str,
        decision: str,
        risk_probability: float,
        reasons: list) -> str:
    """
    Generates a legally compliant adverse action notice
    for every credit risk decision — approved or declined.

    Parameters:
        applicant_reference: unique application ID
        decision: APPROVED or DECLINED
        risk_probability: model probability score
        reasons: list of plain English reason strings

    Returns:
        Formatted notice as a string
    """

    date_today = datetime.now().strftime("%Y-%m-%d")
    separator  = "=" * 65

    notice = f"""
{separator}
CREDIT RISK ASSESSMENT — ADVERSE ACTION NOTICE
{separator}
Applicant Reference: {applicant_reference}
Decision:            {decision}
Risk Probability:    {risk_probability:.1%}
Assessment Date:     {date_today}
{"-" * 65}
"""

    if decision == "DECLINED":
        notice += "\nPrimary reasons for this decision:\n\n"
        for i, reason in enumerate(reasons, 1):
            notice += f"  {i}. {reason}\n"
        notice += f"""
This decision was made by an explainable AI system.
Every factor listed above is traceable and auditable.
You have the right to request a full review of this decision.
"""
    else:
        notice += "\nPrimary strengths supporting this decision:\n\n"
        for i, reason in enumerate(reasons, 1):
            notice += f"  {i}. {reason}\n"
        notice += f"""
This decision was made by an explainable AI system.
Every factor listed above is traceable and auditable.
Congratulations — please proceed to loan documentation.
"""

    notice += separator

    return notice