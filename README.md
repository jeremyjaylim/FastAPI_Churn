# **README.md**

## **Customer Churn Prediction API: FastAPI & Docker Deployment**

An end-to-end MLOps implementation that containerizes a Customer Churn Prediction machine learning model using **FastAPI**, **Docker**, and an **MLflow Model Registry**. This project transitions a trained model tagged with the *@champion* alias in MLflow into a live REST API that provides real-time churn probabilities and business recommendations.

### **📌 Project Overview**

This repository demonstrates how to serve real-time predictions via a FastAPI web service, package the application using Docker for portability, and dynamically connect to an MLflow Model Registry for model serving.

### **📁 Repository Structure**

```
lab-10/
├── main.py              # FastAPI application & business rules engine
├── Dockerfile           # Multi-stage container build specification
├── pyproject.toml       # Environment dependencies managed via uv
├── uv.lock              # Lockfile for deterministic resolution
├── memo.md              # Executive decision memo
└── README.md            # Repository documentation
```

### **🚀 Setup Guide**

#### **1\. Prerequisites**

* Docker Desktop installed and running.  
* Python 3.12 with uv installed.  
* Active MLflow Tracking Server on port 5001\.

#### **2\. Local Execution**

```shell
uv sync
$env:MLFLOW_TRACKING_URI="http://localhost:5001"
uv run uvicorn main:app --reload
```

#### **3\. Containerized Execution**

```shell
docker build -t churn-api:v1 .
docker run -p 8000:8000 -e MLFLOW_TRACKING_URI=http://host.docker.internal:5001 churn-api:v1
```

### **📈 Business Rules & Adaptation**

Raw probability scores guide customer success: scores \> 0.70 are HIGH risk (priority call), 0.40 \- 0.70 are MEDIUM risk (flag for manager), and \< 0.40 are LOW risk. To adapt this repo, update *MODEL\_URI*, the Pydantic *CustomerRecord* model, and the threshold logic in *main.py*.

**Model Deployment with FastAPI and Docker**.

Markdown  
\# Customer Churn Prediction API: FastAPI & Docker Deployment

An end-to-end MLOps implementation that containerizes a Customer Churn Prediction machine learning model using **\*\*FastAPI\*\***, **\*\*Docker\*\***, and an **\*\*MLflow Model Registry\*\***. 

This project transitions a trained model tagged with the \`@champion\` alias in MLflow from a static prototype into a live, portable REST API. The API accepts real-time customer data, computes churn probabilities, and outputs actionable business recommendations based on configurable risk thresholds.

\---

\#\# 📌 Project Overview

In production, machine learning models cannot rely on manual script execution. They must be accessible to external business systems such as CRMs, outreach platforms, and customer dashboards via standardized API endpoints. 

This repository demonstrates how to:  
1\. **\*\*Serve Real-Time Predictions:\*\*** Expose a model via a FastAPI web service.  
2\. **\*\*Containerize for Portability:\*\*** Package the application inside a Docker container to eliminate "it works on my machine" issues across local and cloud environments.  
3\. **\*\*Decouple Serving from Registry:\*\*** Connect the serving container dynamically to an MLflow Model Registry using environment variables and aliases (\`@champion\`).

\---

\#\# 📁 Repository Structure & File Purpose

\`\`\`text  
lab-10/  
├── main.py              \# FastAPI application & business rules engine  
├── Dockerfile           \# Multi-stage container build specification  
├── pyproject.toml       \# Environment dependencies managed via uv  
├── uv.lock              \# Lockfile ensuring deterministic dependency resolution  
├── memo.md              \# Executive decision memo for senior leadership  
└── README.md            \# Repository documentation and setup guide

📑 Detailed File Descriptions

* **main.py**

  * **Purpose:** The core web application script. It initializes FastAPI, connects to the MLflow tracking server using MLFLOW\_TRACKING\_URI, and loads the registered model defined by MODEL\_URI ("models:/churn-prediction-prod@champion") once at startup.  
  * **Data Contracts:** Defines two Pydantic schema models:  
    * CustomerRecord: Strict input validation shape (tenure\_months, monthly\_charges, num\_products, support\_calls\_90d, days\_since\_last\_login).  
    * PredictionResponse: Standardized output response structure (churn\_probability, risk\_level, recommendation).  
  * **Business Engine:** Translates raw probability scores into operational actions via customizable threshold cutoffs.  
* **Dockerfile**

  * **Purpose:** Instructs Docker on how to build the container image.  
  * **Architecture:** Uses python:3.12-slim as a lightweight base image, installs uv for package management, copies pyproject.toml first to leverage Docker layer caching, syncs dependencies, copies application code, exposes port 8000, and launches Uvicorn.  
* **pyproject.toml & uv.lock**

  * **Purpose:** Manages external Python dependencies (fastapi, uvicorn, mlflow, scikit-learn) ensuring identical environment builds across any machine.  
* **memo.md**

  * **Purpose:** An executive memo (400–600 words) written for stakeholders. It addresses business risk trade-offs (False Positives vs. False Negatives), production API security controls, model governance workflows, and enterprise cloud infrastructure (e.g., Azure ML Managed Online Endpoints / Kubernetes).

⚙️ Networking & Architecture

Plaintext  
┌─────────────────────────────────────────────────────────────┐  
│                      Docker Container                       │  
│  ┌──────────────┐     ┌──────────────────────────────────┐  │  
│  │   FastAPI    │ ──\> │ Pydantic Validation & Business   │  │  
│  │ (/predict)   │     │ Risk Logic (HIGH / MED / LOW)    │  │  
│  └──────────────┘     └──────────────────────────────────┘  │  
└─────────│───────────────────────────────────────────────────┘  
          │ (Fetches @champion model via REST API)  
          ▼  
┌─────────────────────────────────────────────────────────────┐  
│                     Host Infrastructure                     │  
│  ┌───────────────────────────────────────────────────────┐  │  
│  │  MLflow Tracking & Model Registry (Port 5001\)         │  │  
│  └───────────────────────────────────────────────────────┘  │  
└─────────────────────────────────────────────────────────────┘

**Important Host Networking Note:**

* When running the API directly on your host machine: set MLFLOW\_TRACKING\_URI=http://127.0.0.1:5001.  
* When running inside a Docker container: set MLFLOW\_TRACKING\_URI=http://host.docker.internal:5001 so the container can route back out to the host system where MLflow runs.

🚀 Reusability Guide: How to Run This Project  
1\. Prerequisites

* Docker Desktop installed and running.  
* Python 3.12 with uv installed.  
* An active MLflow Tracking Server running on port 5001 with a model registered under churn-prediction-prod tagged with the @champion alias.

2\. Local Execution (Development Mode)

> 1. Sync local dependencies:  
>    PowerShell  
>    uv sync

> 2. Start the API locally:  
>    PowerShell  
>    $env:MLFLOW\_TRACKING\_URI\="http://localhost:5001"  
>    uv run uvicorn main:app \-\-reload

> 3. Open your browser to access the health check at http://localhost:8000/ or interactive documentation at http://localhost:8000/docs.

3\. Containerized Execution (Docker)

> 1. Build the Docker image:  
>    PowerShell  
>    docker build \-t churn\-api:v1 .

> 2. Launch the container, configuring host network routing:  
>    PowerShell  
>    docker run \-p 8000:8000 \-e MLFLOW\_TRACKING\_URI=\[http://host.docker.internal:5001\](http://host.docker.internal:5001) churn\-api:v1

📊 Expected Outputs  
1\. Health Check (GET /)

* **Request:** GET http://localhost:8000/

* **Expected Response (200 OK):**

  JSON  
  {  
    "status": "ok",  
    "model": "Churn Prediction API",  
    "version": "1.0.0"  
  }

2\. High-Risk Customer Prediction (POST /predict)

* **Request:** POST http://localhost:8000/predict

* **Sample Payload:**

  JSON  
  {  
    "tenure\_months": 3,  
    "monthly\_charges": 95.0,  
    "num\_products": 1,  
    "support\_calls\_90d": 7,  
    "days\_since\_last\_login": 45  
  }

* **Expected Response (200 OK):**

  JSON  
  {  
    "churn\_probability": 0.8521,  
    "risk\_level": "HIGH",  
    "recommendation": "Priority call within 24 hours. Offer retention package."  
  }

3\. Low-Risk Customer Prediction (POST /predict)

* **Request:** POST http://localhost:8000/predict

* **Sample Payload:**

  JSON  
  {  
    "tenure\_months": 60,  
    "monthly\_charges": 30.0,  
    "num\_products": 4,  
    "support\_calls\_90d": 0,  
    "days\_since\_last\_login": 2  
  }

* **Expected Response (200 OK):**  
  \[cite: 1\]  
  JSON  
  {  
    "churn\_probability": 0.0412,  
    "risk\_level": "LOW",  
    "recommendation": "Standard engagement cadence. No immediate action required."  
  }

📈 Business Rules & Decision Logic  
Raw probability scores are converted into operational risk levels to guide customer success teams\[cite: 1\]:

| Churn Probability | Risk Level | Prescribed Action |
| :---- | :---- | :---- |
| **$\> 0.70$** | HIGH | Priority call within 24 hours. Offer retention package\[cite: 1\]. |
| **$0.40 \- 0.70$** | MEDIUM | Schedule outreach this week. Flag for account manager\[cite: 1\]. |
| **$\< 0.40$** | LOW | Standard engagement cadence. No immediate action required\[cite: 1\]. |

🔄 Adapting This Repo for Custom Models  
If re-using this project layout for a different dataset or MLflow model:

> 1. **Update MODEL\_URI in main.py:** Point to your registered MLflow model name and alias\[cite: 1\].  
> 2. **Update CustomerRecord Pydantic Model:** Adjust fields and data types to match your new model's input feature columns\[cite: 1\].  
> 3. **Update Business Thresholds:** Tailor the if/elif/else probability logic in predict\_churn() according to your specific domain financial trade-offs\[cite: 1\].
