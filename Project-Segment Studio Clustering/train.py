import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import joblib
from getpass import getpass
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# קריאת קובץ הנתונים
df = pd.read_csv('Customers.csv')

# שמירת העמודות שישמשו לבניית האשכולות
selected_columns = [
    'Gender',
    'Age',
    'Annual Income ($)',
    'Spending Score (1-100)',
    'Profession',
    'Work Experience',
    'Family Size'
]

data = df[selected_columns].copy()

# החלפת גיל 0 בערך חסר ולאחר מכן בחציון הגילים
data['Age'] = data['Age'].replace(0, np.nan)
data['Age'] = data['Age'].fillna(data['Age'].median())

# זיהוי עמודות מספריות וקטגוריאליות
numeric_columns = data.select_dtypes(include=np.number).columns.tolist()
categorical_columns = data.select_dtypes(exclude=np.number).columns.tolist()

# מילוי ערכים חסרים בעמודות מספריות באמצעות החציון
for column in numeric_columns:
    data[column] = data[column].fillna(data[column].median())

# מילוי ערכים חסרים בעמודות קטגוריאליות באמצעות הערך הנפוץ ביותר
for column in categorical_columns:
    most_common_value = data[column].value_counts().index[0]
    data[column] = data[column].fillna(most_common_value)

# המרת עמודות קטגוריאליות לעמודות מספריות
encoded_data = pd.get_dummies(data, drop_first=True)

# נרמול הנתונים
scaler = StandardScaler()
scaled_data = scaler.fit_transform(encoded_data)

df_scaled = pd.DataFrame(
    scaled_data,
    columns=encoded_data.columns,
    index=data.index
)

# חישוב WCSS עבור K בין 2 ל-10
k_values = range(2, 11)
wcss_values = []

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(df_scaled)
    wcss_values.append(kmeans.inertia_)

wcss_table = pd.DataFrame({
    'k': list(k_values),
    'WCSS': wcss_values
})

print(wcss_table)

# הצגת גרף Elbow
plt.plot(wcss_table['k'], wcss_table['WCSS'], marker='o')
plt.xlabel('Number of clusters (K)')
plt.ylabel('WCSS')
plt.title('Elbow Method')
plt.xticks(list(k_values))
plt.grid()
plt.show()

# אימון המודל לפי K שנבחר לאחר בדיקת גרף Elbow
selected_k = 9

kmeans_model = KMeans(
    n_clusters=selected_k,
    random_state=42,
    n_init=10
)

kmeans_model.fit(df_scaled)
cluster_labels = kmeans_model.labels_

# שמירת המודל המאומן
joblib.dump(kmeans_model, 'kmeans_model.pkl')

# יצירת טבלה עם מספר הלקוחות בכל אשכול
cluster_table = pd.Series(cluster_labels).value_counts().sort_index().reset_index()
cluster_table.columns = ['cluster_id', 'count']
cluster_table['name'] = ''
cluster_table['description'] = ''

# הוספת מזהה האשכול לנתונים הנקיים
clustered_data = data.copy()
clustered_data['cluster_id'] = cluster_labels

# חישוב ממוצע העמודות המספריות בכל אשכול
numeric_summary = (clustered_data.groupby('cluster_id')[numeric_columns].mean().round(2).reset_index())

# מציאת הערך הנפוץ ביותר בעמודות הקטגוריאליות בכל אשכול
categorical_summary_rows = []

for cluster_id in range(selected_k):
    cluster_rows = clustered_data[clustered_data['cluster_id'] == cluster_id]
    category_values = {'cluster_id': cluster_id}

    for column in categorical_columns:
        category_values[column] = cluster_rows[column].value_counts().index[0]

    categorical_summary_rows.append(category_values)

categorical_summary = pd.DataFrame(categorical_summary_rows)

# איחוד כל נתוני הסיכום לטבלה אחת
cluster_summary = cluster_table[['cluster_id', 'count']].merge(numeric_summary, on='cluster_id')

cluster_summary = cluster_summary.merge(categorical_summary, on='cluster_id')

print(cluster_summary)

# קבלת מפתח Ollama בלי להציג אותו על המסך
api_key = getpass('Enter your Ollama API key: ')

# שליחת הסיכום של כל אשכול ל-Ollama
for row_number, row in cluster_summary.iterrows():
    prompt = 'Analyze this customer cluster using only the information below.\n\n'

    for column in row.index:
        prompt = prompt + f'{column}: {row[column]}\n'

    prompt = prompt + '\nReturn exactly two lines in English:\n'
    prompt = prompt + 'Name: a short name for the cluster\n'
    prompt = prompt + 'Description: one short sentence describing the cluster'

    response = requests.post(
        'https://ollama.com/api/chat',
        headers={
            'Authorization': f'Bearer {api_key}'
        },
        json={
            'model': 'gpt-oss:120b',
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'stream': False,
            'options': {
                'temperature': 0.7
            }
        }
    )

    response_data = response.json()
    response_text = response_data['message']['content']
    lines = response_text.splitlines()

    name = lines[0].replace('Name:', '').strip()
    description = lines[1].replace('Description:', '').strip()
    cluster_id = row['cluster_id']

    cluster_table.loc[cluster_table['cluster_id'] == cluster_id,'name'] = name

    cluster_table.loc[cluster_table['cluster_id'] == cluster_id,'description'] = description

    print('Finished cluster:', cluster_id)

print(cluster_table)

# התאמת שם האשכול לכל לקוח
cluster_name_map = cluster_table.set_index('cluster_id')['name']
cluster_names = []

for cluster_id in cluster_labels:
    cluster_names.append(cluster_name_map[cluster_id])

# הוספת שם האשכול לקובץ המקורי ושמירת התוצאה
result_data = df.copy()
result_data['cluster_name'] = cluster_names
result_data.to_csv('Customers_clustered.csv', index=False)

print('Customers_clustered.csv was created successfully')