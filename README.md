# Credit Risk ML System

Production-grade machine learning system for automated credit risk assessment built on the German Credit Dataset.

Author: Aluka Precious Oluchukwu  
Machine Learning Engineer — Port Harcourt, Nigeria  

Live Demo  
https://aluka-credit-risk-ml-system-production-2036.up.railway.app

GitHub Repository  
https://github.com/Aluka-Analysis/credit-risk-ml-system

---

# Project Overview

This system predicts the probability of loan default for a credit applicant and returns an instant approval or decline decision.

A bank officer submits an application through a professional web dashboard and receives:

• Decision (Approved / Declined)  
• Probability of default  
• Risk classification  
• Key decision reasons  
• Explainable feature contributions  

The model uses Gradient Boosting and explainable AI techniques to ensure transparency and regulatory compliance.

---

# Live Demo

Try the deployed system:

https://aluka-credit-risk-ml-system-production-2036.up.railway.app

The demo allows users to simulate a bank officer submitting a loan application and receiving a real-time credit decision.

---

# System Architecture

```
Bank Officer Input
        │
        ▼
Web Interface (HTML / CSS / JavaScript)
        │
        ▼
FastAPI Inference Service
        │
        ▼
Feature Preprocessing
(StandardScaler)
        │
        ▼
Gradient Boosting Classifier
        │
        ▼
SHAP Explainability Engine
        │
        ▼
Decision + Risk Score + Reasons
        │
        ▼
Displayed instantly on the dashboard
```

---

# System Interface

The system provides a professional loan risk assessment dashboard where a bank officer enters applicant information and receives an immediate decision.

Example output includes:

• Decision status  
• Probability of default  
• Risk level classification  
• Key drivers of the prediction  
• Timestamp and reference ID  

---

# Phases Completed

The project was developed using a structured machine learning lifecycle.

Phase 1 — Project Setup and Architecture  
Phase 2 — Exploratory Data Analysis  
Phase 3 — Feature Engineering  
Phase 4 — Model Training and Evaluation  
Phase 5 — SHAP Explainability and Fairness Analysis  
Phase 6 — FastAPI Inference Service and Frontend  
Phase 7 — Docker Containerisation and Railway Deployment  
Phase 8 — Model Card and Documentation  

---

# Model Performance

| Metric | Value |
|------|------|
| Algorithm | Gradient Boosting Classifier |
| AUC-ROC | 0.7869 |
| Recall | 0.6667 |
| Precision | 0.5479 |
| F1 Score | 0.6015 |
| Optimal Threshold | 0.30 |
| Training Dataset | German Credit Dataset |
| Dataset Size | 1000 applicants |
| Features Used | 17 |

The model threshold was optimised to maximise financial savings rather than accuracy alone, reflecting real-world banking decision strategies.

---

# Fairness and Responsible AI

Credit decision systems must comply with fairness regulations.

Three protected attributes were removed from the model after fairness evaluation.

| Attribute | Reason |
|------|------|
| Status and Sex | Disparate Impact Ratio 0.28 (failed fairness threshold) |
| Foreign Worker | Protected nationality attribute |
| Age in Years | Proxy discrimination detected after sex removal |

Removing these attributes:

• Preserved model performance  
• Increased financial savings by 10,303 DM  
• Improved fairness compliance  

This demonstrates that fairness and profitability are not in conflict in credit risk modelling.

---

# Key Visualisations

## Business Cost Analysis

![Business Cost Analysis](data/processed/18_business_cost_analysis.png)

---

## Fairness Analysis

![Fairness Analysis](data/processed/19_fairness_analysis.png)

---

## SHAP Global Feature Importance

![SHAP Importance](data/processed/14_shap_global_importance.png)

These visualisations provide transparency into model behaviour and fairness evaluation.

---

# API Endpoints

| Endpoint | Method | Description |
|------|------|------|
| / | GET | Frontend dashboard |
| /predict | POST | Credit risk prediction |
| /health | GET | System health check |
| /model-info | GET | Model metadata |
| /docs | GET | Interactive API documentation |

Interactive documentation is automatically generated through Swagger UI.

---

# Technology Stack

| Category | Tools |
|------|------|
| Programming Language | Python 3.11 |
| Machine Learning | Scikit-learn, Imbalanced-learn |
| Explainability | SHAP |
| Backend API | FastAPI, Uvicorn |
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Deployment | Docker, Railway |
| Version Control | Git, GitHub |

---

# Local Installation

Clone the repository:

```
git clone https://github.com/Aluka-Analysis/credit-risk-ml-system.git
cd credit-risk-ml-system
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the API:

```
uvicorn src.api.main:app --reload
```

Open the system:

```
http://localhost:8000
```

---

# Running with Docker

Build the container:

```
docker build -t credit-risk-system .
```

Run the system:

```
docker run -p 8000:8000 credit-risk-system
```

Then open:

```
http://localhost:8000
```

---

# Project Structure

```
credit-risk-ml-system/

├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training_v2.ipynb
│   └── 04_shap_explainability.ipynb
│
├── src/
│   └── api/
│       ├── main.py
│       ├── predict.py
│       ├── schemas.py
│       └── adverse_action.py
│
├── models/
│   ├── credit_risk_production_model.pkl
│   ├── optimal_threshold.pkl
│   └── scaler.pkl
│
├── frontend/
│   └── index.html
│
├── data/
│   ├── raw/
│   └── processed/
│
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

# Business Impact

This system demonstrates how machine learning can support financial institutions by:

• Automating credit risk assessment  
• Reducing manual underwriting workload  
• Improving decision consistency  
• Enabling explainable AI for regulatory compliance  

It illustrates how machine learning models can support real financial decision workflows.

---

# Limitations

• Dataset contains only 1000 applicants  
• Real banking systems require larger datasets  
• Model should be retrained periodically to avoid model drift  
• Additional fairness monitoring is recommended

---

# Future Improvements

Potential production enhancements:

• Prediction logging database  
• Model monitoring and drift detection  
• Authentication for bank officers  
• Feature store integration  
• Cloud autoscaling deployment  

---

# Author

Aluka Precious Oluchukwu  
Machine Learning Engineer  

LinkedIn  
https://www.linkedin.com/in/aluka-precious-b222a2356

GitHub  
https://github.com/Aluka-Analysis
