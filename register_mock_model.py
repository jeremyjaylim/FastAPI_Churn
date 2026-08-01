##this is a mock up python program to perform experiment since i lost the lab08 programdocker ps

import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Point to your local MLflow tracking server
mlflow.set_tracking_uri("http://127.0.0.1:5001")

# Create sample customer data matching main.py's 5 features:
# [tenure_months, monthly_charges, num_products, support_calls_90d, days_since_last_login]
X = np.array([
    [3, 95.0, 1, 7, 45],    # High churn risk
    [60, 30.0, 4, 0, 2],    # Low churn risk
    [12, 70.0, 2, 3, 15],   # Medium risk
    [1, 100.0, 1, 10, 60],  # High churn risk
    [48, 40.0, 3, 1, 5]     # Low churn risk
])
y = np.array([1, 0, 0, 1, 0])  # 1 = Churn, 0 = Stay

# Train a simple classifier
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X, y)

# Register model in MLflow
model_name = "churn-prediction-prod"

with mlflow.start_run():
    mlflow.sklearn.log_model(
        sk_model=clf,
        artifact_path="model",
        registered_model_name=model_name
    )

# Assign the @champion alias required by main.py
client = mlflow.tracking.MlflowClient()
client.set_registered_model_alias(
    name=model_name,
    alias="champion",
    version="1"
)

print(f"\nSuccess! Created and registered '{model_name}' version 1 with alias '@champion'.")