# Segment Studio — Unsupervised Data Clustering System 🚀

<p align="center">
  <img src="segment_studio_banner.png" alt="Segment Studio banner" width="760">
</p>

---

## ✅ Project Status — COMPLETED

**Segment Studio** is an interactive Streamlit application for discovering meaningful groups inside unlabeled CSV data.

**סטודיו לפילוח** הוא אתר אינטראקטיבי להעלאת קובצי CSV ללא עמודת מטרה, בחירת פיצ'רים, זיהוי קבוצות דומות, יצירת שמות והורדת התוצאה.

## 🌐 Render Deployment / Live Application 

The application has been successfully deployed on Render.

🚀 **[Open Segment Studio](https://segment-studio-b588.onrender.com)**

המערכת עלתה בהצלחה וזמינה כעת לשימוש ישירות דרך הדפדפן.

---

## 🎯 Project Goal / מטרת הפרויקט

The application performs a complete unsupervised machine-learning process:

1. Select an example dataset or upload a CSV file.
2. Choose the columns used for clustering.
3. Handle missing values and encode categorical columns.
4. Normalize the features using `StandardScaler`.
5. Compare K values using WCSS and Silhouette Score.
6. Create clusters using `KMeans`.
7. Generate cluster names and descriptions with Ollama.
8. Download the final clustered CSV file.

המערכת מבצעת תהליך מלא של למידה בלתי מונחית: הכנת נתונים, נרמול, בחירת מספר האשכולות, יצירת אשכולות, יצירת שמות באמצעות מודל שפה והורדת קובץ התוצאות.

---

## 🏆 Completed Bonuses / בונוסים שבוצעו

| Bonus | Status | Implementation |
|---|:---:|---|
| **Silhouette Score** | ✅ Completed | A score is calculated for every tested K and displayed in a table and graph. |
| **Automatic K — Silhouette** | ✅ Completed | The K with the highest Silhouette Score is selected automatically. |
| **Automatic K — WCSS with LLM** | ✅ Completed | WCSS values are sent to Ollama, which selects K according to the Elbow Method. |
| **Outlier Removal** | ✅ Completed | Points with an unusually large distance from their cluster center are removed before final training. |
| **Render Deployment — Extra** | ✅ Completed | The complete Streamlit application is available through a public Render URL. |

### ⭐ Extra Enhancement — PCA Visualization

PCA reduces the normalized features to two visual components, `PC1` and `PC2`. The application displays a colored two-dimensional graph and the percentage of variance represented by both components.

PCA משמש להצגה גרפית בלבד ואינו משנה את תהליך האימון או את תוצאות K-Means.

---

## 🧠 Machine-Learning Process

```text
CSV Data → Data Cleaning → Encoding → StandardScaler
         → WCSS + Silhouette → K Selection → Outlier Removal
         → K-Means → PCA Visualization → Ollama Names → CSV Download
```

---

## 📊 Included Example Datasets

| Dataset | Rows | Description |
|---|---:|---|
| `Customers.csv` | 2,000 | Customer demographics, income and spending information |
| `ecommerce.csv` | 350 | E-commerce customer information |
| `iris_unlabaled.csv` | 150 | Unlabeled iris flower measurements |

The user can also drag and drop a personal CSV file into the application.

---

## 📁 Main Files

| File | Purpose                                                          |
|---|------------------------------------------------------------------|
| `train.py` | Demonstrates the complete training process using `Customers.csv` |
| `app.py` | Main Streamlit application                                       |
| `app_bonus.py` | Extended application containing all bonuses and PCA              |
| `requirements.txt` | Required Python packages                                         |
| `segment_studio_banner.png` | Application banner image                                         |
| `kmeans_model.pkl` | Saved K-Means model                                              |
| `project02_clusters_dec25.pdf` | Project requirements and assignment instructions                                                    |

 
---

## 💻 How to Run Locally / הפעלה מקומית

1. Open the terminal inside the project directory.

2. Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

3. Run the complete bonus application:

```powershell
python -m streamlit run app_bonus.py
```

4. Streamlit will open the application in the browser.

---

## 🔑 Ollama API

Ollama is used for selecting K from the WCSS values and for generating a short name and description for every cluster.

Enter the API key only in the protected password field inside the application. Never save an API key inside the code or upload it to GitHub.

---

## 🤖 AI Assistance / שימוש בעזרת AI

ChatGPT and OpenAI Codex were used as learning and development assistants for:

- Guidance related to documentation and docstrings.
- Identifying errors and suggesting code corrections.
- Improving explanations and project documentation.
- Supporting debugging and testing during development.

The project code, results and suggested corrections were reviewed, tested and understood by the student before submission.

נעשה שימוש ב-ChatGPT וב-OpenAI Codex לצורך סיוע בתיעוד וב-docstrings, איתור שגיאות, הצעת תיקונים, שיפור הסברים ותמיכה בתהליך הבדיקות. הקוד והתיקונים נבדקו והובנו לפני ההגשה.

---


## 🛠 Technologies

`Python` · `Streamlit` · `Pandas` · `NumPy` · `Matplotlib` · `Scikit-learn` · `Joblib` · `Ollama API`

---

## 🎉 Final Result

The complete application supports CSV upload, preprocessing, clustering evaluation, automatic K selection, outlier removal, PCA visualization, AI-generated cluster names and final CSV download.
