"""Train and save the loan-approval SVC Pipeline.

The model uses seven features, including credit score.

Target values:
1 = Approved
0 = Rejected
"""

import time
from datetime import timedelta
import joblib
import pandas as pd
from feature_processing import loan_to_income_ratio

from sklearn.metrics import (accuracy_score,classification_report,confusion_matrix)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


NUMERIC_FEATURES = [
    "person_age",
    "person_income",
    "loan_amnt",
    "loan_int_rate",
    "loan_percent_income",
    "credit_score"
]

CATEGORICAL_FEATURES = ["previous_loan_defaults_on_file"]

FEATURES = (NUMERIC_FEATURES + CATEGORICAL_FEATURES)

TARGET_COLUMN = "loan_status"


def load_and_prepare_data():
    """Load the dataset, validate its columns, and prepare it for training."""

    frame = pd.read_csv("Loan_Data.csv")

    frame.columns = (frame.columns.str.strip())

    required_columns = (FEATURES + [TARGET_COLUMN] )

    missing_columns = [
        column
        for column in required_columns
        if column not in frame.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing dataset columns: {missing_columns}"        )

    data = (frame[required_columns].dropna().copy())
    if (data["person_income"] <= 0).any():
        raise ValueError("Income must be positive to calculate the loan ratio")
    data["loan_percent_income"] = loan_to_income_ratio(
        data["loan_amnt"], data["person_income"]
    )

    data["previous_loan_defaults_on_file"] = (
        data["previous_loan_defaults_on_file"]
        .astype(str)
        .str.strip()
        .str.title()
        .map({"No": 0,"Yes": 1})
    )

    if data["previous_loan_defaults_on_file"].isna().any():
        raise ValueError("The defaults column contains values other than Yes or No")

    target_values = set(data[TARGET_COLUMN].unique())

    if not target_values.issubset({0, 1}):
        raise ValueError("loan_status must contain only 0 (Rejected) and 1 (Approved)")

    features = data[FEATURES]
    labels = data[TARGET_COLUMN]

    return features, labels


def build_pipeline():
    """Create the StandardScaler and SVC Pipeline."""

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier",SVC(
                kernel="rbf",
                C=1.0,
                probability=True,
                random_state=42)
        )
    ])

    return pipeline


def evaluate_model(model, test_features, test_labels):
    """Evaluate the model and print its performance metrics."""

    predictions = model.predict(test_features)

    matrix = confusion_matrix(test_labels, predictions)

    accuracy = accuracy_score(test_labels, predictions)

    report = classification_report(test_labels, predictions, zero_division=0)

    print(f"\n🎯 Confusion Matrix:\n {matrix}")

    print(f"\n🎯 Accuracy: {accuracy:.4f}")

    print(f"\n🎯 Classification Report:\n {report}")


def main():
    """Train, evaluate, and save the complete Pipeline."""

    features, labels = (load_and_prepare_data())

    (x_train, x_test, y_train, y_test) = train_test_split(
        features,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )

    print(f"📊 Total rows: {len(features)}")

    print(f"📊 Training samples: {len(x_train)}")

    print(f"📊 Testing samples: {len(x_test)}")

    print("🚀 Training the model, please wait...")

    pipeline = build_pipeline()

    started_at = time.time()

    pipeline.fit(x_train, y_train)

    elapsed_time = timedelta(seconds=int(time.time() - started_at))

    print(f"\n✓ Training completed in {elapsed_time}")

    evaluate_model(pipeline, x_test, y_test)

    joblib.dump(pipeline, "loan_svc_model_v1.0.pkl")

    print("\n💾 Model saved successfully as loan_svc_model_v1.0.pkl")

if __name__ == "__main__":
    main()
