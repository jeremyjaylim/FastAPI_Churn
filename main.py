# lab-10/main.py
# Churn Prediction API
# This FastAPI application loads a trained model from MLflow and serves predictions.
import os
import mlflow.sklearn
from fastapi import FastAPI
from pydantic import BaseModel

# ── YOUR CONFIGURATION ─────────────────────────────────────────────
# Update MODEL_URI to point to your registered model from Lab 8.
# Format: "models:/churn-prediction-prod@champion"
# Replace "churn-prediction-prod" with whatever you named your model.
MODEL_URI = "models:/churn-prediction-prod@champion"
APP_TITLE = "Churn Prediction API"
APP_VERSION = "1.0.0"
# This must point at the same MLflow server from Lab 8 (http://localhost:5001 by default).
# Without this, MLflow looks for the model in a brand-new local
# store instead of your Lab 8 registry, and load_model below fails with
# "Registered Model with name=... not found". Override with the
# MLFLOW_TRACKING_URI environment variable if you ran Lab 8's server on a
# different port.
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5001"))
# ───────────────────────────────────────────────────────────────────

app = FastAPI(title=APP_TITLE, version=APP_VERSION)

# Model cache
_model_cache = None


def get_model():
    """Load model once and cache it."""
    global _model_cache
    if _model_cache is None:
        try:
            _model_cache = mlflow.sklearn.load_model(MODEL_URI)
        except Exception as e:
            raise RuntimeError(f"Failed to load model from {MODEL_URI}: {str(e)}") from e
    return _model_cache


class CustomerRecord(BaseModel):
    """The shape of data this API accepts. Every field is required."""
    tenure_months: int  # how long the customer has been with you
    monthly_charges: float  # their current monthly bill
    num_products: int  # how many products/services they use
    support_calls_90d: int  # support calls in the last 90 days
    days_since_last_login: int  # engagement signal


class PredictionResponse(BaseModel):
    """The shape of data this API returns."""
    churn_probability: float  # 0.0 = very unlikely to churn, 1.0 = very likely
    risk_level: str  # "LOW", "MEDIUM", or "HIGH"
    recommendation: str  # plain-language action for the outreach team


@app.get("/")
def health_check():
    """A simple check that the API is running."""
    return {"status": "ok", "model": APP_TITLE, "version": APP_VERSION}


@app.post("/predict", response_model=PredictionResponse)
def predict_churn(customer: CustomerRecord):
    """
    Given a customer record, return a churn probability and recommendation.
    The outreach team calls this endpoint before prioritizing their calls.
    """
    model = get_model()
    
    features = [[
        customer.tenure_months,
        customer.monthly_charges,
        customer.num_products,
        customer.support_calls_90d,
        customer.days_since_last_login,
    ]]
    probability = model.predict_proba(features)[0][1]
    # ── BUSINESS RULES: translate probability into action ──────────
    # These thresholds are set to balance outreach capacity with customer risk.
    # HIGH risk means the model is confident enough (>= 70%) that the customer is
    # likely to churn and merits immediate retention outreach.
    # MEDIUM risk covers the next tier (>= 40%) so the team can prioritize follow-up
    # without generating too many false positives.
    if probability >= 0.80:
        risk_level = "HIGH"
        recommendation = "Priority call within 24 hours. Offer retention package."
    elif probability >= 0.20:
        risk_level = "MEDIUM"
        recommendation = "Schedule outreach this week. Flag for account manager."
    else:
        risk_level = "LOW"
        recommendation = "Standard engagement cadence. No immediate action required."
    # ───────────────────────────────────────────────────────────────
    return PredictionResponse(
        churn_probability=round(probability, 4),
        risk_level=risk_level,
        recommendation=recommendation,
    )
