import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import json
import shap

# Load dataset - fix path to point to parent directory
dataset_path = os.path.join(os.path.dirname(__file__), "..", "loan_approval_dataset.csv")
df = pd.read_csv(dataset_path)

# Clean column names by stripping whitespace
df.columns = df.columns.str.strip()

# Handle missing values
df = df.dropna()  # Remove rows with any missing values

# Separate features and target
X = df.drop(columns=["loan_id", "loan_status"])
y = df["loan_status"].str.strip().map({"Approved": 1, "Rejected": 0})  # Encode target with string cleaning

# Identify categorical and numeric features
categorical_features = ["education", "self_employed"]
numeric_features = [col for col in X.columns if col not in categorical_features]

# Preprocessing pipeline
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])
categorical_transformer = Pipeline(steps=[
    ('encoder', OneHotEncoder(drop="first"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42, n_estimators=100))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model.fit(X_train, y_train)

# Calculate feature importance
feature_names = numeric_features + [f"{cat}_{val}" for cat, vals in 
                                  zip(categorical_features, 
                                      [model.named_steps['preprocessor'].named_transformers_['cat'].named_steps['encoder'].categories_[0][1:],
                                       model.named_steps['preprocessor'].named_transformers_['cat'].named_steps['encoder'].categories_[1][1:]])
                                  for val in vals]

feature_importance = model.named_steps['classifier'].feature_importances_
feature_importance_dict = dict(zip(feature_names, feature_importance.tolist()))

# Save model - ensure model directory exists and save to correct path
model_dir = os.path.join(os.path.dirname(__file__), "model")
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "loan_approval_pipeline.pkl")
joblib.dump(model, model_path)

# Save feature importance
feature_importance_path = os.path.join(model_dir, "feature_importance.json")
with open(feature_importance_path, 'w') as f:
    json.dump(feature_importance_dict, f, indent=2)

# Calculate and save evaluation metrics
train_accuracy = model.score(X_train, y_train)
test_accuracy = model.score(X_test, y_test)

eval_metrics = {
    "train_accuracy": train_accuracy,
    "test_accuracy": test_accuracy,
    "feature_importance": feature_importance_dict
}

eval_metrics_path = os.path.join(model_dir, "eval_metrics.json")
with open(eval_metrics_path, 'w') as f:
    json.dump(eval_metrics, f, indent=2)

print("✅ Model trained and saved to model/loan_approval_pipeline.pkl")
print(f"Accuracy on training set: {train_accuracy:.4f}")
print(f"Accuracy on test set: {test_accuracy:.4f}")
print("✅ Feature importance saved to model/feature_importance.json")
print("✅ Evaluation metrics saved to model/eval_metrics.json")
