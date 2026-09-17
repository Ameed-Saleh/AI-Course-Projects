# Loan Approval Prediction System 🚀

A machine-learning project that predicts loan approval using a Support Vector
Classifier (SVC), with a Flask website, an analytics dashboard, and a REST API.
The interface supports **Hebrew and English**, including right-to-left layout.

The project connects data preparation, model training, input validation,
prediction, and evaluation in one educational application.

## 🌐 Render Deployment — Bonus Task

| Page | Hosted application |
|---|---|
| Prediction form / בדיקת זכאות | [Open application](https://loan-approval-prediction-ij1y.onrender.com/) |
| Model dashboard / מדדי המודל | [Open dashboard](https://loan-approval-prediction-ij1y.onrender.com/dashboard) |

These are the project's supplied deployment links. Local changes appear on the
hosted application only after the updated project is deployed to Render.

## Main Features

- Loan classification with an estimated probability for the predicted class.
- Automatic calculation of the loan-to-income ratio.
- Input validation in the browser and on the server, with localized messages.
- Dashboard with performance metrics, confusion matrix, class distribution and charts.
- General indicators and suggestions based on the applicant's inputs.
- Download of the trained model, including its fitted scaler.

## Dataset and Target

Dataset reference: [Loan Approval Classification Dataset on Kaggle](https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data).
The local file, `Loan_Data.csv`, contains **45,000 records**.

The target is `loan_status`: **1 = Approved**, **0 = Rejected**, following the
dataset documentation.

The dataset is synthetic. Predictions reflect learned patterns and do not
represent actual lending decisions or guarantee approval. Higher income alone
does not guarantee a positive prediction. Displayed suggestions are general
rules, not a direct explanation of the SVC's decision.

## Seven Model Features

Users enter **six values**; the seventh feature is calculated automatically.

| Feature | Meaning | Input |
|---|---|---|
| `person_age` | Applicant age | Manual; whole number, 20–80 |
| `person_income` | Annual income in dollars | Manual |
| `loan_amnt` | Requested loan amount in dollars | Manual |
| `loan_int_rate` | Interest rate in percent | Manual |
| `loan_percent_income` | Loan amount divided by annual income | Automatic |
| `credit_score` | Applicant credit score | Manual; whole number, 390–850 in the current data |
| `previous_loan_defaults_on_file` | Previous default: No = 0, Yes = 1 | Manual selection |

For example, a $10,000 loan and $100,000 annual income produce a ratio of `0.10`,
displayed as **10%**. Training, evaluation and prediction use the unrounded ratio;
rounding is only for display.

The form and server share numeric limits. The calculated ratio is also checked
against the dataset range. Changing income or loan amount updates its validation.

## Model and Evaluation

The saved scikit-learn `Pipeline` contains:

1. **StandardScaler** — scales features using statistics fitted only on training data.
2. **SVC** — uses an RBF kernel, `C=1.0`, `gamma="scale"`, and probability estimation.

A stratified split preserves class proportions: **36,000 training records (80%)**
and **9,000 test records (20%)**, with `random_state=42`.

The most recent locally verified evaluation produced:

| Metric | Result |
|---|---:|
| Accuracy | 90.48% |
| Precision — class 1 | 80.45% |
| Recall — class 1 | 75.50% |
| F1-score — class 1 | 77.90% |

Confusion matrix: rows are actual classes; columns are predicted classes.

| Actual / Predicted | Predicted 0 | Predicted 1 |
|---|---:|---:|
| Actual 0 | 6,633 — TN | 367 — FP |
| Actual 1 | 490 — FN | 1,510 — TP |

The dashboard calculates metrics from the loaded model and dataset. Retraining
or changing the data can change these results.

### Dashboard Illustration

The two-dimensional decision plot uses a **separate linear SVC** fitted on two
PCA components derived from the seven features. Point colors show that model's
predictions; the solid line shows its boundary, dashed lines show its margins,
and hollow circles identify support vectors.

This plot illustrates SVM separation. Website predictions and the reported
evaluation metrics use the saved **RBF model**.

## Project Structure

```text
Loan_Project/
├── app.py                     # Flask routes, validation, predictions and metrics
├── train.py                   # Train, evaluate and save the model
├── feature_processing.py      # Shared loan-to-income calculation
├── Loan_Data.csv              # Dataset
├── Loan_Data-Model.ipynb       # Training notebook without function definitions
├── loan_svc_model_v1.0.pkl     # Saved scaler + SVC Pipeline
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── .gitignore                 # Excludes local environment and cache files
└── templates/
    ├── index.html             # Prediction form
    ├── dashboard.html         # Analytics and charts
    └── error.html             # Service-unavailable page
```

## Run Locally

Open a terminal inside `Loan_Project`. These Windows PowerShell commands use the
virtual environment directly, so activation is not required.

**1. Create the environment and install dependencies:**

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**2. Train and save the model:**

```powershell
.\.venv\Scripts\python.exe train.py
```

Training replaces `loan_svc_model_v1.0.pkl` and prints evaluation results.
This step is optional if a compatible trained model is already present.

The notebook provides an alternative training workflow. Use a Jupyter kernel
with the same package versions as the website. If loading reports a version
mismatch, retrain in the website's environment before relying on the saved model.

**3. Start the website:**

```powershell
.\.venv\Scripts\python.exe app.py
```

- [Local prediction form](http://127.0.0.1:5000/)
- [Local dashboard](http://127.0.0.1:5000/dashboard)

Local links work while the server is running. Startup includes computing
dashboard data and may take a short while. Restart the server after retraining
or changing Python code. Keep the dataset, model and `feature_processing.py`
in the project directory.

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/model/info` | Features, configuration, metrics, samples and chart data |
| `GET` | `/api/metrics-chart` | Plotly chart specification for class metrics |
| `POST` | `/api/model/predict` | Validate details and return a prediction |
| `POST` | `/predict` | Alias for the prediction endpoint |
| `GET` | `/download/model` | Download the trained Pipeline |


## Recent Improvements and Verification

- Added credit score, bringing the model to seven features.
- Unified the unrounded ratio calculation across training, evaluation and prediction.
- Aligned form and server limits, enforced whole-number age and credit score,
  and added checks for the calculated ratio.
- Handled oversized numbers and blocked prediction when validation data is missing.
- Clarified the dashboard illustration in both languages, documented Python
  functions, and cleaned up dependencies and README formatting.

Local checks covered valid predictions, eight examples spanning all four
confusion-matrix outcomes, and invalid inputs such as credit score `9999`, age
`100`, fractional age, zero income and out-of-range ratios. Browser checks covered
language switching, chart loading, and clearing ratio errors after correcting
inputs. The eight selected examples demonstrate coverage; overall accuracy is
measured on the complete test set.
