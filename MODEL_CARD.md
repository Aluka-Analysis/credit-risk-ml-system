# Model Card — Credit Risk ML System

**Model Name:** Credit Risk Gradient Boosting Classifier  
**Version:** 3.0.0  
**Date:** March 2026  
**Author:** Aluka Precious Oluchukwu — Machine Learning Engineer  
**Contact:** https://www.linkedin.com/in/aluka-precious-b222a2356 

---

## Model Description

A production-grade credit risk assessment model built on the 
German Credit Dataset. The model predicts the probability that 
a loan applicant will default on their loan obligation.

The system is designed for use by bank officers to support — 
not replace — human credit decisions. Every prediction comes 
with a plain English explanation and a legally compliant 
adverse action notice.

---

## Intended Use

**Primary use:**  
Credit risk assessment for loan applications in a supervised 
banking environment where a trained officer reviews every 
decision.

**Intended users:**  
Bank officers and credit analysts using the system as a 
decision support tool.

**Out of scope uses:**  
- Fully automated loan decisions without human review
- Use outside of supervised banking environments
- Assessment of loan applicants in jurisdictions with 
  different regulatory frameworks without review
- Any use that treats model output as final without 
  human oversight

---

## Training Data

| Attribute | Details |
|-----------|---------|
| Dataset | German Credit Dataset |
| Source | UCI Machine Learning Repository |
| Size | 1000 loan applicants |
| Period | 1990s — West Germany |
| Target | Binary — Good Risk (0) vs Bad Risk (1) |
| Class Distribution | 700 Good Risk (70%) / 300 Bad Risk (30%) |

**Important data limitation:**  
The training data is from 1990s Germany. Patterns learned 
from this data may not fully represent modern lending 
environments or applicants from other regions.

---

## Features Used

17 features after removing protected attributes:

| Feature | Type | Description |
|---------|------|-------------|
| Checking account status | Categorical | Current account balance status |
| Duration in month | Numerical | Loan duration in months |
| Credit history | Categorical | History of credit repayment |
| Purpose | Categorical | Purpose of the loan |
| Credit amount | Numerical | Loan amount requested |
| Savings account/bonds | Categorical | Savings level |
| Employment | Categorical | Employment duration |
| Installment | Numerical | Installment rate as % of income |
| Other debtors/guarantors | Categorical | Guarantor status |
| Residence | Numerical | Years at current residence |
| Property | Categorical | Property ownership |
| Other installment plans | Categorical | Existing installment plans |
| Housing | Categorical | Housing status |
| Existing credits | Numerical | Number of existing credits |
| Job | Categorical | Job type |
| Liability responsibles | Numerical | Number of dependants |
| Telephone | Categorical | Telephone registration status |

---

## Protected Attributes Removed

Three protected attributes were removed from model training 
after fairness analysis:

| Attribute | Reason for Removal |
|-----------|-------------------|
| Status and Sex | Disparate Impact Ratio 0.28 — failed 0.80 regulatory threshold. Model was systematically overpredicting bad risk for female applicants due to representation bias in 1990s training data |
| Foreign Worker | Legally protected nationality attribute under ECOA, GDPR, and CBN Consumer Protection Framework |
| Age in Years | Proxy discrimination detected — after removing sex, model redistributed predictive weight onto age causing DIR to fall below 0.80 threshold |

**Key finding:**  
Removing protected attributes caused zero performance loss 
and increased financial savings by 10,303 DM — proving 
fairness and profitability are not in conflict.

---

## Model Architecture

| Component | Details |
|-----------|---------|
| Algorithm | Gradient Boosting Classifier |
| Pipeline | StandardScaler → Gradient Boosting |
| SMOTE | Applied inside cross validation folds only — not in production pipeline |
| Tuning | RandomizedSearchCV — 50 iterations × 5 folds |
| Version Control | v1 (20 features) → v2 (18 features) → v3 (17 features — current) |

---

## Performance Metrics

Evaluated on a clean holdout test set of 200 applicants 
never seen during training or tuning.

| Metric | Value |
|--------|-------|
| AUC-ROC | 0.7869 |
| Accuracy | 0.7350 |
| Recall (Bad Risk) | 0.6667 |
| Precision (Bad Risk) | 0.5479 |
| F1 Score | 0.6015 |
| Optimal Threshold | 0.30 |

**Threshold justification:**  
Threshold lowered from 0.50 to 0.30 based on business cost 
analysis. Missing a bad risk borrower costs the bank the 
entire loan amount. Wrongly declining a good customer costs 
only the interest foregone. The asymmetric cost structure 
justifies a more conservative threshold.

---

## Business Impact

At optimal threshold 0.30 compared to no screening:

| Scenario | Bad Risks Caught | Losses Prevented | Net Benefit |
|----------|-----------------|-----------------|-------------|
| No Model | 0 | 0 DM | 0 DM |
| Threshold 0.50 | 34 | 66,728 DM | 63,457 DM |
| Threshold 0.30 | 40 | 78,504 DM | 73,107 DM |

---

## Explainability

Every prediction includes:
- Risk probability score
- SHAP feature contribution chart
- Top 3 plain English reasons for the decision
- Legally compliant adverse action notice

SHAP — SHapley Additive exPlanations — assigns each feature 
a contribution score for every individual prediction, 
satisfying both technical and regulatory interpretability 
requirements.

---

## Fairness Analysis

| Protected Attribute | Disparate Impact Ratio | Status |
|--------------------|----------------------|--------|
| Status and Sex | 0.28 | Removed — failed threshold |
| Foreign Worker | 0.45 | Removed — legally protected |
| Age in Years | Failed after sex removal | Removed — proxy discrimination |

Fairness auditing should be repeated if the model is 
retrained on new data.

---

## Limitations

1. **Data age:** Training data is from 1990s Germany. 
   Economic conditions and lending practices have changed 
   significantly since then.

2. **Geographic specificity:** Model was trained on German 
   credit data. Performance may differ significantly for 
   applicants from other regions.

3. **Class imbalance:** Original dataset had 70/30 split. 
   SMOTE was used during training to address this. 
   Real world default rates may differ.

4. **Feature encoding:** Categorical features were Label 
   Encoded. This may introduce implicit ordinal relationships 
   that do not exist in reality.

5. **No temporal validation:** Model was validated on a 
   random holdout split not an out-of-time split. 
   Performance on future data may differ.

---

## Ethical Considerations

- Model must never be used as the sole basis for credit 
  decisions without human review
- Regular fairness audits are recommended — at minimum 
  annually or when model is retrained
- Adverse action notices must be provided to every 
  declined applicant as required by law
- Model should not be deployed in jurisdictions where 
  the regulatory framework differs significantly from 
  ECOA and GDPR without legal review

---

## Retraining Recommendations

The model should be retrained when:
- AUC-ROC drops below 0.72 on new data
- Significant changes in economic conditions occur
- New regulatory requirements affect feature usage
- Data drift is detected in key features
- More than 12 months have passed since last training

---

## Regulatory Compliance

This model was designed with the following frameworks 
in mind:

- **ECOA** — Equal Credit Opportunity Act
- **GDPR** — General Data Protection Regulation  
- **CBN** — Central Bank of Nigeria Consumer 
  Protection Framework

---

## Citation
```
Aluka Precious Oluchukwu (2026)
Credit Risk ML System — German Credit Dataset
Machine Learning Engineer
Port Harcourt, Nigeria
GitHub: https://github.com/Aluka-Analysis/credit-risk-ml-system
```

---

*This model card follows the Model Cards for Model Reporting 
framework proposed by Mitchell et al. (2019)*