import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier
)
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

import joblib
import os


# ============================================================
# 1. LOAD PROCESSED DATASET
# ============================================================

DATA_FILE = "dataset/pookalam_processed.csv"

df = pd.read_csv(DATA_FILE)

print("=" * 70)
print("POOKALAM RECOMMENDATION MODEL TRAINING")
print("=" * 70)

print("\nDataset shape:", df.shape)


# ============================================================
# 2. BASIC VALIDATION
# ============================================================

required_columns = [
    "design_id",
    "budget",
    "theme",
    "style",
    "layers",
    "difficulty",
    "primary_flower",
    "secondary_flower",
    "accent_flower",
    "primary_color",
    "secondary_color",
    "accent_color",
    "diameter_ft",
    "estimated_time_hr",
    "people_required",
    "occasion",
    "flower_diversity",
    "color_diversity",
    "estimated_flower_cost"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("✓ All required columns are present")


if df["design_id"].duplicated().sum() > 0:
    raise ValueError(
        "Duplicate design IDs found."
    )

print("✓ Design IDs are unique")


if df.isna().sum().sum() > 0:
    raise ValueError(
        "Missing values found in dataset."
    )

print("✓ No missing values")


# ============================================================
# 3. DATASET INFORMATION
# ============================================================

print("\nNumber of designs:", len(df))

print("\nTheme distribution:")
print(
    df["theme"].value_counts()
)


# ============================================================
# 4. CREATE RECOMMENDATION SCORE
# ============================================================

def calculate_base_score(row):

    score = 50

    # --------------------------------------------------------
    # Difficulty
    # --------------------------------------------------------

    if row["difficulty"] == "Easy":
        score += 10

    elif row["difficulty"] == "Medium":
        score += 5

    # --------------------------------------------------------
    # Diameter
    # --------------------------------------------------------

    if row["diameter_ft"] <= 6:
        score += 5

    # --------------------------------------------------------
    # Flower diversity
    # --------------------------------------------------------

    if row["flower_diversity"] >= 3:
        score += 5

    # --------------------------------------------------------
    # Color diversity
    # --------------------------------------------------------

    if row["color_diversity"] >= 2:
        score += 5

    # --------------------------------------------------------
    # Budget efficiency
    # --------------------------------------------------------

    if row["budget"] > 0:

        cost_ratio = (
            row["estimated_flower_cost"]
            / row["budget"]
        )

        if cost_ratio <= 0.70:
            score += 10

        elif cost_ratio <= 0.90:
            score += 5

    return min(score, 100)


df["recommendation_score"] = df.apply(
    calculate_base_score,
    axis=1
)


# ============================================================
# 5. CREATE RECOMMENDATION CATEGORY
# ============================================================

def assign_category(score):

    if score >= 80:
        return "Excellent"

    elif score >= 65:
        return "Good"

    elif score >= 50:
        return "Moderate"

    else:
        return "Low"


df["recommendation_category"] = (
    df["recommendation_score"]
    .apply(assign_category)
)


print("\nRecommendation distribution:")
print(
    df["recommendation_category"]
    .value_counts()
)


# ============================================================
# 6. MACHINE LEARNING FEATURES
# ============================================================

features = [
    "budget",
    "theme",
    "style",
    "layers",
    "difficulty",
    "primary_flower",
    "secondary_flower",
    "accent_flower",
    "primary_color",
    "secondary_color",
    "accent_color",
    "diameter_ft",
    "estimated_time_hr",
    "people_required",
    "occasion",
    "flower_diversity",
    "color_diversity",
    "estimated_flower_cost"
]

X = df[features]

y = df["recommendation_category"]


# ============================================================
# 7. NUMERICAL FEATURES
# ============================================================

numerical_features = [
    "budget",
    "layers",
    "diameter_ft",
    "estimated_time_hr",
    "people_required",
    "flower_diversity",
    "color_diversity",
    "estimated_flower_cost"
]


# ============================================================
# 8. CATEGORICAL FEATURES
# ============================================================

categorical_features = [
    "theme",
    "style",
    "difficulty",
    "primary_flower",
    "secondary_flower",
    "accent_flower",
    "primary_color",
    "secondary_color",
    "accent_color",
    "occasion"
]


# ============================================================
# 9. PREPROCESSOR
# ============================================================

preprocessor = ColumnTransformer(

    transformers=[

        (
            "num",
            StandardScaler(),
            numerical_features
        ),

        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )

    ]
)


# ============================================================
# 10. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 11. MODELS
# ============================================================

models = {

    "Logistic Regression":
        LogisticRegression(
            max_iter=2000,
            random_state=42
        ),

    "Decision Tree":
        DecisionTreeClassifier(
            max_depth=6,
            min_samples_leaf=5,
            random_state=42
        ),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=300,
            max_depth=8,
            min_samples_leaf=3,
            random_state=42
        ),

    "Gradient Boosting":
        GradientBoostingClassifier(
            n_estimators=150,
            max_depth=3,
            learning_rate=0.05,
            random_state=42
        )
}


# ============================================================
# 12. TRAIN MODELS
# ============================================================

results = []

trained_models = {}


for name, model in models.items():

    print("\n" + "=" * 70)
    print("Training:", name)
    print("=" * 70)

    pipeline = Pipeline(

        steps=[

            (
                "preprocessor",
                preprocessor
            ),

            (
                "model",
                model
            )

        ]
    )


    pipeline.fit(
        X_train,
        y_train
    )


    y_pred = pipeline.predict(
        X_test
    )


    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )


    print("\nAccuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))


    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0
        )
    )


    results.append({

        "Model": name,

        "Accuracy": accuracy,

        "Precision": precision,

        "Recall": recall,

        "F1 Score": f1

    })


    trained_models[name] = pipeline


# ============================================================
# 13. MODEL COMPARISON
# ============================================================

results_df = pd.DataFrame(
    results
)

results_df = results_df.sort_values(
    by="F1 Score",
    ascending=False
)


print("\n")
print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

print(
    results_df.to_string(
        index=False
    )
)


# ============================================================
# 14. SELECT BEST MODEL
# ============================================================

best_model_name = (
    results_df
    .iloc[0]["Model"]
)

best_model = trained_models[
    best_model_name
]


print("\n")
print("=" * 70)
print("BEST MODEL")
print("=" * 70)

print(
    "Selected model:",
    best_model_name
)


# ============================================================
# 15. CREATE MODELS DIRECTORY
# ============================================================

os.makedirs(
    "models",
    exist_ok=True
)


# ============================================================
# 16. SAVE BEST MODEL
# ============================================================

MODEL_FILE = (
    "models/best_recommendation_model.pkl"
)

joblib.dump(
    best_model,
    MODEL_FILE
)

print(
    "\nBest recommendation model saved:"
)

print(
    MODEL_FILE
)


# ============================================================
# 17. SAVE MODEL COMPARISON
# ============================================================

RESULT_FILE = (
    "recommendation_model_comparison.csv"
)

results_df.to_csv(
    RESULT_FILE,
    index=False
)

print(
    "\nModel comparison saved:"
)

print(
    RESULT_FILE
)


# ============================================================
# 18. SAVE TRAINING INFORMATION
# ============================================================

training_info = {

    "dataset_size": len(df),

    "number_of_features": len(features),

    "features": features,

    "best_model": best_model_name,

    "best_accuracy":
        results_df.iloc[0]["Accuracy"],

    "best_precision":
        results_df.iloc[0]["Precision"],

    "best_recall":
        results_df.iloc[0]["Recall"],

    "best_f1":
        results_df.iloc[0]["F1 Score"]

}

print("\nTraining information:")
print(
    training_info
)


# ============================================================
# COMPLETE
# ============================================================

print("\n")
print("=" * 70)
print("RECOMMENDATION MODEL TRAINING COMPLETED")
print("=" * 70)