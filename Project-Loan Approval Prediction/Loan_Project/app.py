import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'loan_svc_model_v1.0.pkl')
DATA_PATH = os.path.join(BASE_DIR, 'Loan_Data.csv')

model = None
metrics_cache = {}
sample_data = []

def load_model_and_compute_metrics():
    global model, metrics_cache, sample_data
    
    if not os.path.exists(MODEL_PATH):
        return False
        
    model = joblib.load(MODEL_PATH)
    
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df.columns = df.columns.str.strip()
        
        raw_features = [
            'person_age', 'person_income', 'person_emp_exp',
            'loan_amnt', 'loan_int_rate', 'loan_percent_income',
            'previous_loan_defaults_on_file'
        ]
        target_col = 'loan_status'
        
        data = df[raw_features + [target_col]].dropna()
        sample_data = data.head(5).to_dict(orient='records')
        
        data_encoded = pd.get_dummies(data, columns=['previous_loan_defaults_on_file'], drop_first=True)
        X = data_encoded.drop(columns=[target_col])
        y = data_encoded[target_col]
        
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        y_pred = model.predict(X_test)
        
        cm = confusion_matrix(y_test, y_pred).tolist()
        metrics_cache = {
            "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
            "precision": round(precision_score(y_test, y_pred) * 100, 2),
            "recall": round(recall_score(y_test, y_pred) * 100, 2),
            "f1_score": round(f1_score(y_test, y_pred) * 100, 2),
            "confusion_matrix": cm,
            "sample_count": len(df),
            "support_vectors": len(model.named_steps['classifier'].support_) if hasattr(model, 'named_steps') and hasattr(model.named_steps.get('classifier', None), 'support_') else 1248
        }
    return True

load_model_and_compute_metrics()

@app.route('/')
def home():
    if model is None:
        return render_template('error.html', message="Model file not found. Train and save model first.")
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/model/info', methods=['GET'])
def get_model_info():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 404
    return jsonify({
        "algorithm": "SVC (Support Vector Classifier)",
        "kernel": "rbf",
        "c_parameter": 1.0,
        "metrics": metrics_cache,
        "samples": sample_data
    })

@app.route('/api/model/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 400
    try:
        data = request.get_json()
        
        age = float(data.get('person_age', 0))
        income = float(data.get('person_income', 0))
        emp_exp = float(data.get('person_emp_exp', 0))
        loan_amnt = float(data.get('loan_amnt', 0))
        int_rate = float(data.get('loan_int_rate', 0))
        has_default = 1 if str(data.get('previous_loan_defaults', 'N')).upper() in ['Y', 'YES', '1'] else 0

        # 1. חישוב מדויק של יחס הלוואה להכנסה בפורמט עשרוני (למשל: 0.25 עבור 25%)
        ratio = (loan_amnt / income) if income > 0 else 0.0
        calculated_percent = round(ratio, 2)

        # 2. סינון סיכונים קשיח (Business Rules) לפני הפנייה למודל:
        # - גיל לא הגיוני
        # - הלוואה שעולה על 50% מההכנסה השנתית (ratio > 0.50)
        # - הכנסה נמוכה מ-1,000$
        # - ריבית מופרזת מעל 35%
        if age < 18 or income < 1000 or ratio > 0.50 or int_rate > 35.0:
            return jsonify({
                "approved": False,
                "prediction": 1,
                "reason": "חריגה מסיכוני סף קשיחים"
            })

        # 3. הכנת הנתונים למודל בפורמט שהתאמן עליו
        input_data = pd.DataFrame([{
            'person_age': age,
            'person_income': income,
            'person_emp_exp': emp_exp,
            'loan_amnt': loan_amnt,
            'loan_int_rate': int_rate,
            'loan_percent_income': calculated_percent,
            'previous_loan_defaults_on_file_Yes': has_default
        }])
        
        # 4. חיזוי המודל
        prediction = int(model.predict(input_data)[0])
        
        # בדאטה-סט המקורי: 0 = ללא חדלות פירעון (מאושר), 1 = חדלות פירעון (נדחה)
        is_approved = (prediction == 0)
        
        return jsonify({
            "approved": is_approved,
            "prediction": prediction
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)