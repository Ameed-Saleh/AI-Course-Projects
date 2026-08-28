import json
import logging
import os

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.utils
from flask import Flask, jsonify, render_template, request, send_file
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.svm import SVC


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "loan_svc_model_v1.0.pkl")
DATA_PATH = os.path.join(BASE_DIR, "Loan_Data.csv")

FEATURES = [
    "person_age",
    "person_income",
    "loan_amnt",
    "loan_int_rate",
    "loan_percent_income",
    "previous_loan_defaults_on_file",
]
NUMERIC_INPUTS = [
    "person_age",
    "person_income",
    "loan_amnt",
    "loan_int_rate",
]
TARGET_COLUMN = "loan_status"

model = None
metrics_cache = {}
sample_data = []
validation_ranges = {}
validation_medians = {}
chart_data_cache = []
decision_map_cache = {}


@app.after_request
def disable_browser_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response


def encode_defaults(series):
    normalized = series.astype(str).str.strip().str.title()
    encoded = normalized.map({"No": 0, "Yes": 1})
    if encoded.isna().any():
        invalid_values = sorted(normalized[encoded.isna()].unique().tolist())
        raise ValueError(f"Invalid values in previous_loan_defaults_on_file: {invalid_values}")
    return encoded.astype(int)


def load_model_and_compute_metrics():
    global model, metrics_cache, sample_data, validation_ranges, validation_medians, chart_data_cache, decision_map_cache

    if not os.path.exists(MODEL_PATH):
        app.logger.error("Model file not found at %s", MODEL_PATH)
        return False

    try:
        model = joblib.load(MODEL_PATH)
        app.logger.info("Model loaded successfully")
    except Exception:
        app.logger.exception("Could not load model")
        model = None
        return False

    if not os.path.exists(DATA_PATH):
        app.logger.warning("Dataset file not found at %s", DATA_PATH)
        return True

    try:
        df = pd.read_csv(DATA_PATH)
        df.columns = df.columns.str.strip()

        missing_columns = [column for column in FEATURES + [TARGET_COLUMN] if column not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing dataset columns: {missing_columns}")

        data = df[FEATURES + [TARGET_COLUMN]].dropna().copy()
        if data.empty:
            raise ValueError("Dataset has no complete rows")

        raw_samples = data.head(5).copy()
        sample_data = raw_samples.to_dict(orient="records")

        validation_ranges = {
            feature: {
                "min": float(data[feature].min()),
                "max": float(data[feature].max()),
            }
            for feature in FEATURES[:-1]
        }
        validation_medians = {
            feature: float(data[feature].median())
            for feature in FEATURES[:-1]
        }

        data["previous_loan_defaults_on_file"] = encode_defaults(
            data["previous_loan_defaults_on_file"]
        )

        X = data[FEATURES]
        y = data[TARGET_COLUMN]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y,
        )

        y_pred = model.predict(X_test)
        decision_scores = model.decision_function(X_test)
        report = classification_report(
            y_test,
            y_pred,
            output_dict=True,
            zero_division=0,
        )
        matrix = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = matrix.ravel()

        chart_data_cache = [
            {
                "x": round(float(row["loan_percent_income"]), 4),
                "y": round(float(row["loan_int_rate"]), 2),
                "prediction": int(prediction),
                "margin": round(float(score), 4),
            }
            for (_, row), prediction, score in zip(X_test.iterrows(), y_pred, decision_scores)
        ]

        # A dedicated two-dimensional projection for the dashboard. The production
        # model remains the six-feature RBF SVC loaded above; this linear SVC exists
        # only to make its class separation easy to understand visually.
        scaler = model.named_steps["scaler"]
        train_scaled = scaler.transform(X_train)
        test_scaled = scaler.transform(X_test)
        pca = PCA(n_components=2, random_state=42)
        train_2d = pca.fit_transform(train_scaled)
        test_2d = pca.transform(test_scaled)
        visual_svc = SVC(kernel="linear", C=1.0, random_state=42)
        visual_svc.fit(train_2d, y_train)
        visual_predictions = visual_svc.predict(test_2d)

        x_padding = max((test_2d[:, 0].max() - test_2d[:, 0].min()) * 0.08, 0.25)
        y_padding = max((test_2d[:, 1].max() - test_2d[:, 1].min()) * 0.08, 0.25)
        x_min, x_max = test_2d[:, 0].min() - x_padding, test_2d[:, 0].max() + x_padding
        y_min, y_max = test_2d[:, 1].min() - y_padding, test_2d[:, 1].max() + y_padding
        line_x = np.linspace(x_min, x_max, 120)
        weight_x, weight_y = visual_svc.coef_[0]
        intercept = visual_svc.intercept_[0]

        def boundary_line(level):
            if abs(weight_y) < 1e-9:
                x_value = (level - intercept) / weight_x
                return [{"x": round(float(x_value), 4), "y": round(float(y_min), 4)},
                        {"x": round(float(x_value), 4), "y": round(float(y_max), 4)}]
            values = (level - intercept - weight_x * line_x) / weight_y
            return [
                {"x": round(float(x), 4), "y": round(float(y), 4)}
                for x, y in zip(line_x, values)
                if y_min <= y <= y_max
            ]

        visible_support_vectors = [
            point for point in visual_svc.support_vectors_
            if x_min <= point[0] <= x_max and y_min <= point[1] <= y_max
        ]
        if len(visible_support_vectors) > 220:
            support_step = len(visible_support_vectors) / 220
            visible_support_vectors = [
                visible_support_vectors[int(index * support_step)] for index in range(220)
            ]

        decision_map_cache = {
            "points": [
                {"x": round(float(point[0]), 4), "y": round(float(point[1]), 4),
                 "prediction": int(prediction)}
                for point, prediction in zip(test_2d, visual_predictions)
            ],
            "support_vectors": [
                {"x": round(float(point[0]), 4), "y": round(float(point[1]), 4)}
                for point in visible_support_vectors
            ],
            "boundary": boundary_line(0),
            "margin_positive": boundary_line(1),
            "margin_negative": boundary_line(-1),
            "bounds": {"x_min": float(x_min), "x_max": float(x_max),
                       "y_min": float(y_min), "y_max": float(y_max)},
            "explained_variance": round(float(pca.explained_variance_ratio_.sum() * 100), 1),
        }

        metrics_cache = {
            "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
            "precision": round(precision_score(y_test, y_pred, zero_division=0) * 100, 2),
            "recall": round(recall_score(y_test, y_pred, zero_division=0) * 100, 2),
            "f1_score": round(f1_score(y_test, y_pred, zero_division=0) * 100, 2),
            "confusion_matrix": matrix.tolist(),
            "confusion_matrix_details": {
                "tn": int(tn),
                "fp": int(fp),
                "fn": int(fn),
                "tp": int(tp),
            },
            "sample_count": int(len(data)),
            "test_count": int(len(y_test)),
            "support_vectors": int(len(model.named_steps["classifier"].support_)),
            "class_0": {
                "precision": round(report["0"]["precision"] * 100, 2),
                "recall": round(report["0"]["recall"] * 100, 2),
                "f1_score": round(report["0"]["f1-score"] * 100, 2),
                "support": int(report["0"]["support"]),
            },
            "class_1": {
                "precision": round(report["1"]["precision"] * 100, 2),
                "recall": round(report["1"]["recall"] * 100, 2),
                "f1_score": round(report["1"]["f1-score"] * 100, 2),
                "support": int(report["1"]["support"]),
            },
            "macro_avg": {
                "precision": round(report["macro avg"]["precision"] * 100, 2),
                "recall": round(report["macro avg"]["recall"] * 100, 2),
                "f1_score": round(report["macro avg"]["f1-score"] * 100, 2),
            },
            "weighted_avg": {
                "precision": round(report["weighted avg"]["precision"] * 100, 2),
                "recall": round(report["weighted avg"]["recall"] * 100, 2),
                "f1_score": round(report["weighted avg"]["f1-score"] * 100, 2),
            },
        }
        app.logger.info("Model metrics calculated successfully")
        return True
    except Exception:
        app.logger.exception("Could not compute model metrics")
        return False


def localizer(language):
    is_hebrew = str(language).lower().startswith("he")

    def localized(hebrew_text, english_text):
        return hebrew_text if is_hebrew else english_text

    return localized


def error_response(localized, message_he, message_en, status_code=422, field_errors=None):
    return jsonify({
        "status": "error",
        "error": localized(message_he, message_en),
        "field_errors": field_errors or {},
    }), status_code


def parse_numeric_inputs(payload, localized):
    missing_fields = [field for field in NUMERIC_INPUTS if payload.get(field) in (None, "")]
    if missing_fields:
        field_errors = {
            field: localized("שדה חובה.", "This field is required.")
            for field in missing_fields
        }
        response = error_response(
            localized,
            "יש למלא את כל השדות המספריים.",
            "Please complete all numeric fields.",
            field_errors=field_errors,
        )
        return None, response

    try:
        values = {field: float(payload[field]) for field in NUMERIC_INPUTS}
    except (TypeError, ValueError):
        response = error_response(
            localized,
            "יש להזין מספרים תקינים בלבד.",
            "Please enter valid numbers only.",
        )
        return None, response

    invalid_fields = [field for field, value in values.items() if not np.isfinite(value)]
    if invalid_fields:
        field_errors = {
            field: localized("הזינו מספר תקין.", "Enter a valid number.")
            for field in invalid_fields
        }
        response = error_response(
            localized,
            "אחד או יותר מהערכים אינו מספר תקין.",
            "One or more values is not a valid number.",
            field_errors=field_errors,
        )
        return None, response

    return values, None


def parse_previous_default(payload, localized):
    raw_value = payload.get(
        "previous_loan_defaults_on_file",
        payload.get("previous_loan_defaults"),
    )

    if raw_value in (None, ""):
        response = error_response(
            localized,
            "יש לבחור האם היו כשלים קודמים בהחזר הלוואה.",
            "Please select whether there were previous loan defaults.",
            field_errors={
                "previous_loan_defaults_on_file": localized("שדה חובה.", "This field is required.")
            },
        )
        return None, response

    normalized = str(raw_value).strip().lower()
    mapping = {
        "yes": 1,
        "y": 1,
        "1": 1,
        "true": 1,
        "no": 0,
        "n": 0,
        "0": 0,
        "false": 0,
    }

    if normalized not in mapping:
        response = error_response(
            localized,
            "הערך של היסטוריית ההלוואות אינו תקין.",
            "The previous-loan-default value is invalid.",
            field_errors={
                "previous_loan_defaults_on_file": localized("בחרו כן או לא.", "Select Yes or No.")
            },
        )
        return None, response

    return mapping[normalized], None


def validate_input_ranges(values, localized):
    errors = {}

    for field, value in values.items():
        limits = validation_ranges.get(field)
        if not limits:
            continue
        if value < limits["min"] or value > limits["max"]:
            errors[field] = localized(
                f"הערך חייב להיות בין {limits['min']:,.2f} ל-{limits['max']:,.2f}.",
                f"The value must be between {limits['min']:,.2f} and {limits['max']:,.2f}.",
            )

    if errors:
        return error_response(
            localized,
            "חלק מהערכים נמצאים מחוץ לטווח שעליו המודל אומן.",
            "Some values are outside the range used to train the model.",
            field_errors=errors,
        )

    return None


def build_explanation(values, has_default, ratio, localized):
    reasons = []
    recommendations = []

    if has_default:
        reasons.append(localized(
            "נמצאה היסטוריה של כשל קודם בהחזר הלוואה.",
            "A previous loan default was reported.",
        ))
        recommendations.append(localized(
            "מומלץ לבדוק ולשפר את היסטוריית ההחזרים.",
            "Review and improve the repayment history.",
        ))

    if ratio > validation_medians.get("loan_percent_income", ratio):
        reasons.append(localized(
            f"יחס ההלוואה להכנסה גבוה יחסית: {ratio * 100:.2f}%.",
            f"The loan-to-income ratio is relatively high: {ratio * 100:.2f}%.",
        ))
        recommendations.append(localized(
            "אפשר לשקול סכום הלוואה נמוך יותר.",
            "Consider requesting a smaller loan amount.",
        ))

    if values["person_income"] < validation_medians.get("person_income", values["person_income"]):
        reasons.append(localized(
            "ההכנסה נמוכה מחציון ההכנסה בנתוני האימון.",
            "The income is below the training-data median.",
        ))

    if values["loan_int_rate"] > validation_medians.get("loan_int_rate", values["loan_int_rate"]):
        reasons.append(localized(
            "שיעור הריבית גבוה מחציון הריבית בנתוני האימון.",
            "The interest rate is above the training-data median.",
        ))
        recommendations.append(localized(
            "אפשר לבדוק אפשרות לריבית נמוכה יותר.",
            "Check whether a lower interest rate is available.",
        ))

    if not reasons:
        reasons.append(localized(
            "התחזית מבוססת על השילוב בין כל ששת הפיצ'רים.",
            "The prediction is based on the combination of all six features.",
        ))

    if not recommendations:
        recommendations.append(localized(
            "לא זוהתה המלצה כללית על סמך המדדים שנבדקו.",
            "No general recommendation was identified from the inspected indicators.",
        ))

    return reasons, recommendations


load_model_and_compute_metrics()


@app.route("/")
def home():
    if model is None:
        return render_template(
            "error.html",
            message="Model file not found. Train and save the model first.",
        ), 503
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    if model is None:
        return render_template(
            "error.html",
            message="Model file not found. Train and save the model first.",
        ), 503
    return render_template("dashboard.html")


@app.route("/api/model/info", methods=["GET"])
def get_model_info():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 404

    return jsonify({
        "algorithm": "SVC (Support Vector Classifier)",
        "kernel": "rbf",
        "c_parameter": 1.0,
        "feature_count": len(FEATURES),
        "feature_names": FEATURES,
        "metrics": metrics_cache,
        "samples": sample_data,
        "chart_data": chart_data_cache,
        "decision_map": decision_map_cache,
        "validation_ranges": validation_ranges,
    })


@app.route("/api/metrics-chart", methods=["GET"])
def get_metrics_chart():
    if not metrics_cache:
        return jsonify({"error": "Metrics not loaded"}), 404

    chart_df = pd.DataFrame({
        "Metric": ["Precision", "Recall", "F1-Score"] * 2,
        "Score": [
            metrics_cache["class_0"]["precision"],
            metrics_cache["class_0"]["recall"],
            metrics_cache["class_0"]["f1_score"],
            metrics_cache["class_1"]["precision"],
            metrics_cache["class_1"]["recall"],
            metrics_cache["class_1"]["f1_score"],
        ],
        "Class": ["Class 0 (Rejected)"] * 3 + ["Class 1 (Approved)"] * 3,
    })

    figure = px.bar(
        chart_df,
        x="Metric",
        y="Score",
        color="Class",
        barmode="group",
        text="Score",
        title="ביצועי המודל לפי סיווג (Model Metrics by Class)",
        color_discrete_sequence=["#4A90E2", "#50E3C2"],
    )
    figure.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Score: %{y:.2f}%<extra></extra>",
    )
    figure.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Segoe UI, sans-serif", "size": 14, "color": "#333333"},
        title={"font": {"size": 18, "color": "#1A202C"}, "x": 0.5},
        yaxis={"range": [0, 115], "title": "Score (%)", "gridcolor": "#E2E8F0"},
        xaxis={"title": ""},
        legend={"title": "", "orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    )

    return jsonify(json.loads(json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)))


@app.route("/download/model", methods=["GET"])
def download_model():
    if not os.path.exists(MODEL_PATH):
        return jsonify({"error": "Model file not found"}), 404
    return send_file(
        MODEL_PATH,
        as_attachment=True,
        download_name="loan_svc_model_v1.0.pkl",
    )


@app.route("/predict", methods=["POST"])
@app.route("/api/model/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"status": "error", "error": "Model not loaded"}), 503

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"status": "error", "error": "A valid JSON request body is required"}), 400

    localized = localizer(payload.get("language", "he"))

    values, numeric_error = parse_numeric_inputs(payload, localized)
    if numeric_error:
        return numeric_error

    has_default, default_error = parse_previous_default(payload, localized)
    if default_error:
        return default_error

    range_error = validate_input_ranges(values, localized)
    if range_error:
        return range_error

    income = values["person_income"]
    loan_amount = values["loan_amnt"]

    if income <= 0:
        return error_response(
            localized,
            "ההכנסה חייבת להיות גדולה מאפס.",
            "Income must be greater than zero.",
            field_errors={"person_income": localized("הזינו ערך גדול מאפס.", "Enter a value greater than zero.")},
        )

    if loan_amount <= 0:
        return error_response(
            localized,
            "סכום ההלוואה חייב להיות גדול מאפס.",
            "Loan amount must be greater than zero.",
            field_errors={"loan_amnt": localized("הזינו ערך גדול מאפס.", "Enter a value greater than zero.")},
        )

    ratio = loan_amount / income

    model_input = pd.DataFrame([{
        "person_age": values["person_age"],
        "person_income": income,
        "loan_amnt": loan_amount,
        "loan_int_rate": values["loan_int_rate"],
        "loan_percent_income": ratio,
        "previous_loan_defaults_on_file": has_default,
    }], columns=FEATURES)

    try:
        prediction = int(model.predict(model_input)[0])
        probabilities = model.predict_proba(model_input)[0]
        classes = list(model.classes_)
        predicted_probability = round(float(probabilities[classes.index(prediction)]) * 100, 2)
        class_one_probability = round(float(probabilities[classes.index(1)]) * 100, 2)
    except Exception:
        app.logger.exception("Prediction failed")
        return error_response(
            localized,
            "לא ניתן להשלים את התחזית.",
            "The prediction could not be completed.",
            status_code=500,
        )

    approved = prediction == 1
    result_text = "Approved" if approved else "Rejected"
    reasons, recommendations = build_explanation(values, has_default, ratio, localized)

    app.logger.info("Prediction completed: %s", result_text)

    return jsonify({
        "status": "success",
        "approved": approved,
        "prediction": prediction,
        "result_text": result_text,
        "loan_percent_income": round(ratio, 6),
        "loan_percent_income_display": round(ratio * 100, 2),
        "prediction_probability": predicted_probability,
        "class_one_probability": class_one_probability,
        "reasons": reasons,
        "recommendations": recommendations,
        "explanation_note": localized(
            "התוצאה היא תחזית של המודל ואינה התחייבות לאישור הלוואה.",
            "The result is a model prediction and does not guarantee loan approval.",
        ),
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
