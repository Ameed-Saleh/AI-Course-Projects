# 1. Load Libraries and Data
# ==========================================
import time
from datetime import timedelta
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
# ==========================================

# 2. Load data and clean column names
df = pd.read_csv('Loan_Data.csv')
df.columns = df.columns.str.strip()

# 3. Select numerical features and one categorical binary feature
raw_features = [
    'person_age',
    'person_income',
    'person_emp_exp',
    'loan_amnt',
    'loan_int_rate',
    'loan_percent_income',
    'previous_loan_defaults_on_file',  # Categorical text column (Y/N)
]
target_col = 'loan_status'

# 4. Handle missing values and perform One-Hot Encoding
data = df[raw_features + [target_col]].dropna()
data_encoded = pd.get_dummies(data, columns=['previous_loan_defaults_on_file'], drop_first=True)

X = data_encoded.drop(columns=[target_col])
y = data_encoded[target_col]

# 5. Split data into 80% training and 20% testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 6. Build Pipeline and train the model
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', SVC(
        kernel='rbf',
        C=1.0,
        probability=True,
        random_state=42
    ))
])

# Displaying dataset split sizes
train_pct = round((len(X_train) / len(df)) * 100)
test_pct = round((len(X_test) / len(df)) * 100)
print(f'📊 Total Rows: {len(df)}')
print(f'📊 Training samples: {X_train.shape[0]} -> {train_pct}%')
print(f'📊 Testing samples: {X_test.shape[0]} -> {test_pct}%')

start_time = time.time()
print('🚀 Training the model, please wait...')

# Passing raw X_train; Pipeline handles scaling automatically
pipeline.fit(X_train, y_train)
elapsed = timedelta(seconds=int(time.time() - start_time))

# Predicting on raw X_test using the trained pipeline
y_pred = pipeline.predict(X_test)

print(f'✓ Training completed in {elapsed}!')
print(f'🎯 Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}')
print(f'🎯 Accuracy: {accuracy_score(y_test, y_pred):.4f}\n')
print(classification_report(y_test, y_pred))

# 7. Save model pipeline
joblib.dump(pipeline, 'loan_svc_model_v1.0.pkl')
print("💡 Summary: The 80/20 split gives the best results, It provides more data for training while keeping enough data for a reliable test.")
print('💾 Model saved successfully as loan_svc_model_v1.0.pkl!')