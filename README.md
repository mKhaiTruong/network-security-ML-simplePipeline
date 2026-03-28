# Network Security ML Pipeline

A machine learning pipeline for network security threat detection (phishing detection), built with MLOps principles in mind.

---

## Pipeline Overview

```
Data Ingestion → Data Validation → Data Transformation → Model Trainer
```

Each component communicates via **Artifacts** — lightweight objects carrying output paths and metadata to the next stage. No hardcoded paths, no tight coupling.

---

## Components

### 1. Data Ingestion
Pulls raw network traffic data and splits into train/test sets. Standard component, nothing unusual.

### 2. Data Validation
Checks schema, data types, and drift against a reference schema. Ensures garbage doesn't flow downstream.

### 3. Data Transformation
The first interesting component.

**Why KNNImputer?**
Tabular/structured data almost always has missing values. Unlike image data (where you just drop corrupted samples), network traffic logs can have partial entries that still carry signal. KNNImputer fills missing values based on similar rows — better than mean/median imputation for this kind of data.

**Why save the preprocessor?**
The `StandardScaler` and `KNNImputer` *learn* statistics from training data (mean, std, neighbor distances). These stats must be frozen and reused at inference time. If you refit on new data, you get different numbers → model sees input it was never trained on → silent wrong predictions.

This is why `preprocessor.pkl` is saved alongside the model, and why `NetworkModel` wraps both together. At inference: raw data in, prediction out — no manual transform step.

> This is different from CV/vision pipelines where normalization stats (e.g. ImageNet mean/std) are hardcoded. In tabular data, stats come from your specific dataset and must be persisted.

### 4. Model Trainer
The most complex component.

**Models evaluated:** Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, AdaBoost — with GridSearchCV hyperparameter tuning per model.

**Why F1, Precision, and Recall — not R²?**

R² is a regression metric. It measures how well predictions explain variance in a continuous target. Applying it to a binary classification problem (threat / no threat) produces a number that is mathematically valid but meaningfully useless.

For network security classification:

| Metric | What it answers |
|---|---|
| **Precision** | Of all flagged threats, how many were real? (false alarm rate) |
| **Recall** | Of all real threats, how many did we catch? (miss rate) |
| **F1** | Harmonic mean of both — single score balancing the two |

In security contexts, **missing a real threat (low recall) is usually worse** than a false alarm (low precision). F1 gives a balanced view; precision/recall separately tell you *which direction* your model is failing.

**Best model selection:**
`GridSearchCV` returns `best_estimator_` — the already-tuned, already-fitted model. This is extracted directly and used for prediction, avoiding redundant refit calls.

**Overfitting check:**
Train metrics and test metrics are both computed and stored in the artifact. If `train_score >> test_score`, the model is overfitting. This comparison is passed downstream to the Model Evaluation component.

---

## Key Design Decisions

**Artifact-based pipeline** — each component outputs an artifact (file paths + metadata) rather than returning data directly. This makes components independently runnable, testable, and swappable without touching downstream code.

**Preprocessor + Model bundled together** — `NetworkModel(preprocessor, model)` ensures the transformation and inference always stay in sync. Deploy one file, not two.

**MLflow experiment tracking** — model metrics, parameters, and artifacts are logged per run for reproducibility and comparison.

---

## Tech Stack

- `scikit-learn` — preprocessing, models, GridSearchCV
- `MLflow` — experiment tracking
- `numpy` — array storage for transformed data
- `pymongo` — data source (raw ingestion)
