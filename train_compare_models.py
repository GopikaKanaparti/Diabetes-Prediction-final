import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

import joblib


# -------------------------------------------------
# 1. Load Dataset
# -------------------------------------------------
# ⚠️ Change path only if your dataset is elsewhere
data = pd.read_csv("datasets\diabetes.csv")

X = data.drop("Outcome", axis=1)
y = data["Outcome"]

# -------------------------------------------------
# 2. Train-Test Split
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------------------------------
# 3. Define Models
# -------------------------------------------------
models = {
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ]),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42
    ),

    "XGBoost": XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42
    )
}

# -------------------------------------------------
# 4. Train & Evaluate Models
# -------------------------------------------------
results = []

for name, model in models.items():
    print(f"\nTraining {name}...")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    results.append({
        "Model": name,
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1-score": f1
    })

# -------------------------------------------------
# 5. Results Comparison Table
# -------------------------------------------------
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by="F1-score", ascending=False)

print("\n================ MODEL COMPARISON ================\n")
print(results_df.to_string(index=False))

# -------------------------------------------------
# 6. Save Best Model
# -------------------------------------------------
best_model_name = results_df.iloc[0]["Model"]
best_model = models[best_model_name]

joblib.dump(best_model, "best_diabetes_model.pkl")

print("\n==================================================")
print(f"Best Model Selected: {best_model_name}")
print("Saved as: best_diabetes_model.pkl")
print("==================================================")
