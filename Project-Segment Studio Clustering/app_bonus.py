import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA


def prepare_data(df, selected_columns):
    data = df[selected_columns].copy()

    numeric_columns = data.select_dtypes(include=np.number).columns.tolist()
    categorical_columns = data.select_dtypes(exclude=np.number).columns.tolist()

    for column in numeric_columns:
        median_value = data[column].median()

        if pd.isna(median_value):
            median_value = 0

        data[column] = data[column].fillna(median_value)

    for column in categorical_columns:
        value_counts = data[column].value_counts()

        if len(value_counts) == 0:
            most_common_value = 'Unknown'
        else:
            most_common_value = value_counts.index[0]

        data[column] = data[column].fillna(most_common_value)

    encoded_data = pd.get_dummies(data, drop_first=True)

    if encoded_data.shape[1] == 0:
        return data, encoded_data, None, numeric_columns, categorical_columns

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(encoded_data)

    df_scaled = pd.DataFrame(
        scaled_data,
        columns=encoded_data.columns,
        index=data.index
    )

    return data, encoded_data, df_scaled, numeric_columns, categorical_columns


def calculate_clustering_scores(df_scaled, min_k, max_k):
    k_values = range(min_k, max_k + 1)
    wcss_values = []
    silhouette_values = []

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(df_scaled)
        wcss_values.append(kmeans.inertia_)

        if len(np.unique(cluster_labels)) > 1:
            silhouette_value = silhouette_score(df_scaled, cluster_labels)
        else:
            silhouette_value = -1

        silhouette_values.append(silhouette_value)

    score_table = pd.DataFrame({
        'k': list(k_values),
        'WCSS': wcss_values,
        'Silhouette Score': silhouette_values
    })

    return score_table


def select_best_k(score_table):
    best_row_number = score_table['Silhouette Score'].idxmax()
    best_k = int(score_table.loc[best_row_number, 'k'])

    return best_k


def build_wcss_selection_prompt(score_table):
    prompt = (
        'Choose the best K using only the WCSS values below. '
        'Find the elbow point, where the improvement starts becoming much '
        'smaller.\n\n'
    )

    for row_number, row in score_table.iterrows():
        prompt = prompt + (
            f"K: {int(row['k'])}, WCSS: {row['WCSS']:.2f}\n"
        )

    prompt = prompt + '\nReturn exactly one line:\nK: one number'

    return prompt


def create_clusters(df_scaled, selected_k):
    kmeans_model = KMeans(
        n_clusters=selected_k,
        random_state=42,
        n_init=10
    )

    kmeans_model.fit(df_scaled)
    cluster_labels = kmeans_model.labels_

    return kmeans_model, cluster_labels


def create_pca_data(df_scaled, cluster_labels):
    if df_scaled.shape[1] < 2:
        return None, None

    pca = PCA(n_components=2)
    pca_values = pca.fit_transform(df_scaled)

    pca_data = pd.DataFrame({
        'PC1': pca_values[:, 0],
        'PC2': pca_values[:, 1],
        'cluster_id': cluster_labels
    })

    explained_variance = pca.explained_variance_ratio_.sum() * 100

    return pca_data, explained_variance


def remove_outliers(df, data, df_scaled, selected_k):
    first_model, first_labels = create_clusters(df_scaled, selected_k)
    all_distances = first_model.transform(df_scaled)
    row_numbers = np.arange(len(df_scaled))
    distance_to_center = all_distances[row_numbers, first_labels]

    average_distance = distance_to_center.mean()
    distance_standard_deviation = distance_to_center.std()
    outlier_threshold = average_distance + 2 * distance_standard_deviation
    rows_to_keep = distance_to_center <= outlier_threshold

    clean_df = df[rows_to_keep].reset_index(drop=True)
    clean_data = data[rows_to_keep].reset_index(drop=True)
    clean_scaled_data = df_scaled[rows_to_keep].reset_index(drop=True)
    removed_rows = int((rows_to_keep == False).sum())

    return (
        clean_df,
        clean_data,
        clean_scaled_data,
        removed_rows,
        outlier_threshold
    )


def create_cluster_table(cluster_labels):
    cluster_table = (
        pd.Series(cluster_labels)
        .value_counts()
        .sort_index()
        .reset_index()
    )

    cluster_table.columns = ['cluster_id', 'count']
    cluster_table['name'] = ''
    cluster_table['description'] = ''

    return cluster_table


def create_cluster_summary(
    data,
    cluster_labels,
    numeric_columns,
    categorical_columns,
    selected_k
):
    clustered_data = data.copy()
    clustered_data['cluster_id'] = cluster_labels

    cluster_summary = create_cluster_table(cluster_labels)[
        ['cluster_id', 'count']
    ]

    if len(numeric_columns) > 0:
        numeric_summary = (
            clustered_data.groupby('cluster_id')[numeric_columns]
            .mean()
            .round(2)
            .reset_index()
        )

        cluster_summary = cluster_summary.merge(
            numeric_summary,
            on='cluster_id'
        )

    if len(categorical_columns) > 0:
        categorical_summary_rows = []

        for cluster_id in range(selected_k):
            cluster_rows = clustered_data[
                clustered_data['cluster_id'] == cluster_id
            ]
            category_values = {'cluster_id': cluster_id}

            for column in categorical_columns:
                category_values[column] = (
                    cluster_rows[column]
                    .value_counts()
                    .index[0]
                )

            categorical_summary_rows.append(category_values)

        categorical_summary = pd.DataFrame(categorical_summary_rows)

        cluster_summary = cluster_summary.merge(
            categorical_summary,
            on='cluster_id'
        )

    return cluster_summary


def build_cluster_prompt(row):
    prompt = 'Analyze this customer cluster using only the information below.\n\n'

    for column in row.index:
        prompt = prompt + f'{column}: {row[column]}\n'

    prompt = prompt + '\nReturn exactly two lines in English:\n'
    prompt = prompt + 'Name: a short name for the cluster\n'
    prompt = prompt + 'Description: one short sentence describing the cluster'

    return prompt


def ask_ollama(prompt, api_key):
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
    return response_data['message']['content']


def select_k_with_ollama(score_table, api_key):
    prompt = build_wcss_selection_prompt(score_table)
    response_text = ask_ollama(prompt, api_key)
    first_line = response_text.splitlines()[0]
    best_k = int(first_line.replace('K:', '').strip())

    return best_k


def parse_cluster_response(response_text):
    lines = response_text.splitlines()
    name = lines[0].replace('Name:', '').strip()
    description = lines[1].replace('Description:', '').strip()

    return name, description


def name_clusters(cluster_summary, cluster_table, api_key):
    named_cluster_table = cluster_table.copy()

    for row_number, row in cluster_summary.iterrows():
        prompt = build_cluster_prompt(row)
        response_text = ask_ollama(prompt, api_key)
        name, description = parse_cluster_response(response_text)
        cluster_id = row['cluster_id']

        named_cluster_table.loc[
            named_cluster_table['cluster_id'] == cluster_id,
            'name'
        ] = name

        named_cluster_table.loc[
            named_cluster_table['cluster_id'] == cluster_id,
            'description'
        ] = description

    return named_cluster_table


def create_result_data(df, cluster_labels, named_cluster_table):
    cluster_name_map = named_cluster_table.set_index('cluster_id')['name']
    cluster_names = []

    for cluster_id in cluster_labels:
        cluster_names.append(cluster_name_map[cluster_id])

    result_data = df.copy()
    result_data['cluster_name'] = cluster_names

    return result_data


def show_styled_table(table):
    numeric_columns = table.select_dtypes(include=np.number).columns.tolist()

    styled_table = (
        table.style
        .format(precision=2)
        .set_table_styles([
            {
                'selector': 'th',
                'props': [
                    ('background-color', '#5B4BDB'),
                    ('color', 'white'),
                    ('font-weight', 'bold'),
                    ('text-align', 'center')
                ]
            },
            {
                'selector': 'td',
                'props': [
                    ('border-bottom', '1px solid #E8EAF6')
                ]
            }
        ])
    )

    if len(numeric_columns) > 0:
        styled_table = styled_table.background_gradient(
            cmap='Blues',
            subset=numeric_columns
        )

    table_height = min(430, 38 * (len(table) + 1))

    st.dataframe(
        styled_table,
        use_container_width=True,
        hide_index=True,
        height=table_height
    )


def show_elbow_chart(wcss_table):
    figure, axis = plt.subplots(figsize=(7, 3.8))
    figure.patch.set_facecolor('#F7F8FC')
    axis.set_facecolor('#F7F8FC')
    axis.plot(
        wcss_table['k'],
        wcss_table['WCSS'],
        color='#5B4BDB',
        marker='o',
        markerfacecolor='#FF6B6B',
        linewidth=2.5
    )
    axis.set_xlabel('Number of clusters (K)')
    axis.set_ylabel('WCSS')
    axis.set_title('Elbow Method')
    axis.set_xticks(wcss_table['k'])
    axis.grid(alpha=0.25)
    figure.tight_layout()

    chart_column, empty_column = st.columns([2, 1])

    with chart_column:
        st.pyplot(figure, use_container_width=False)


def show_silhouette_chart(score_table):
    figure, axis = plt.subplots(figsize=(7, 3.8))
    figure.patch.set_facecolor('#F7F8FC')
    axis.set_facecolor('#F7F8FC')
    axis.plot(
        score_table['k'],
        score_table['Silhouette Score'],
        color='#37B98B',
        marker='o',
        markerfacecolor='#52B6FF',
        linewidth=2.5
    )
    axis.set_xlabel('Number of clusters (K)')
    axis.set_ylabel('Silhouette Score')
    axis.set_title('Silhouette Score by K')
    axis.set_xticks(score_table['k'])
    axis.grid(alpha=0.25)
    figure.tight_layout()

    chart_column, empty_column = st.columns([2, 1])

    with chart_column:
        st.pyplot(figure, use_container_width=False)


def show_pca_chart(pca_data):
    figure, axis = plt.subplots(figsize=(7, 4.5))
    figure.patch.set_facecolor('#F7F8FC')
    axis.set_facecolor('#F7F8FC')

    cluster_ids = sorted(pca_data['cluster_id'].unique())

    for cluster_id in cluster_ids:
        cluster_rows = pca_data[
            pca_data['cluster_id'] == cluster_id
        ]

        axis.scatter(
            cluster_rows['PC1'],
            cluster_rows['PC2'],
            label=f'Cluster {cluster_id}',
            color=plt.cm.tab10(int(cluster_id) % 10),
            alpha=0.7,
            s=35
        )

    axis.set_xlabel('Principal Component 1')
    axis.set_ylabel('Principal Component 2')
    axis.set_title('PCA Cluster Visualization')
    axis.grid(alpha=0.2)
    axis.legend(title='Clusters', bbox_to_anchor=(1.02, 1), loc='upper left')
    figure.tight_layout()

    chart_column, empty_column = st.columns([2, 1])

    with chart_column:
        st.pyplot(figure, use_container_width=False)


def clear_cluster_results():
    cluster_keys = [
        'cluster_labels',
        'cluster_table',
        'cluster_summary',
        'original_data',
        'original_file_name',
        'result_data',
        'outlier_count',
        'outlier_threshold',
        'outlier_cleaning_used',
        'original_row_count',
        'cleaned_row_count',
        'pca_data',
        'pca_explained_variance'
    ]

    for key in cluster_keys:
        if key in st.session_state:
            del st.session_state[key]


def clear_analysis_results():
    analysis_keys = ['score_table', 'score_columns']

    for key in analysis_keys:
        if key in st.session_state:
            del st.session_state[key]

    clear_cluster_results()


def reset_results():
    clear_analysis_results()

    control_keys = [
        'min_k_input',
        'max_k_input',
        'selected_k_input',
        'remove_outliers_input',
        'automatic_k_method',
        'wcss_api_key'
    ]

    for key in control_keys:
        if key in st.session_state:
            del st.session_state[key]


def synchronize_min_k():
    if st.session_state['min_k_input'] > st.session_state['max_k_input']:
        st.session_state['max_k_input'] = st.session_state['min_k_input']

    clear_analysis_results()


def synchronize_max_k():
    if st.session_state['max_k_input'] < st.session_state['min_k_input']:
        st.session_state['min_k_input'] = st.session_state['max_k_input']

    clear_analysis_results()


def apply_custom_style():
    st.markdown(
        '''
        <style>
        .main-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 1.4rem;
            letter-spacing: 0.3px;
        }

        .title-english {
            background: linear-gradient(90deg, #52B6FF, #6C63FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .title-divider {
            color: #8B7CF6;
            padding: 0 12px;
        }

        .title-hebrew {
            background: linear-gradient(90deg, #37D5A5, #52B6FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .explanation-title-english {
            color: #52A7FF;
            font-size: 1.12rem;
            font-weight: 700;
            margin: 1rem 0 0.35rem 0;
        }

        .explanation-title-hebrew {
            color: #41D59A;
            font-size: 1.12rem;
            font-weight: 700;
            margin: 1rem 0 0.35rem 0;
            direction: rtl;
            text-align: right;
        }

        .process-line {
            font-size: 1.04rem;
            font-weight: 700;
            line-height: 2;
            margin: 1rem 0 0.5rem 0;
        }

        .process-title {
            color: #52A7FF;
        }

        .process-title-hebrew {
            color: #41D59A;
        }

        .process-arrow {
            color: #7A8399;
            padding: 0 5px;
        }

        .process-step-1 { color: #8EDBFF; }
        .process-step-2 { color: #6BC9FF; }
        .process-step-3 { color: #52B3FF; }
        .process-step-4 { color: #6494FF; }
        .process-step-5 { color: #7478F2; }
        .process-step-6 { color: #865FDC; }
        .process-step-7 { color: #A64FC7; }

        [data-testid="stImage"] img {
            border-radius: 18px;
            box-shadow: 0 12px 35px rgba(47, 93, 170, 0.28);
        }

        [data-testid="stHeaderActionElements"] {
            display: none;
        }

        </style>
        ''',
        unsafe_allow_html=True
    )


def main():
    st.set_page_config(page_title='Segment Studio', layout='wide')
    apply_custom_style()

    st.markdown(
        '''
        <div class="main-title">
            <span class="title-english">Segment Studio</span>
            <span class="title-divider">|</span>
            <span class="title-hebrew" dir="rtl">סטודיו לפילוח</span>
        </div>
        ''',
        unsafe_allow_html=True
    )

    image_left, image_center, image_right = st.columns([1, 4, 1])

    with image_center:
        st.image('segment_studio_banner.png', use_container_width=True)

    st.markdown(
        '<div class="explanation-title-english">What is Segment Studio?</div>',
        unsafe_allow_html=True
    )

    st.info(
        'Discover similar groups in CSV data, name each group and download the '
        'clustered result.'
    )

    st.markdown(
        '<div class="explanation-title-hebrew">מהו סטודיו לפילוח?</div>',
        unsafe_allow_html=True
    )

    st.success(
        'סטודיו לפילוח הוא כלי שמזהה קבוצות דומות בתוך נתונים ללא חלוקה מוקדמת. '
        'המשתמש בוחר קובץ ועמודות, בוחן את מספר הקבוצות המתאים, יוצר את הקבוצות, '
        'מעניק להן שמות ומוריד קובץ מעודכן.'
    )

    st.markdown(
        '''
        <div class="process-line">
            <span class="process-title">Process</span>
            <span class="title-divider">|</span>
            <span class="process-title-hebrew" dir="rtl">תהליך</span>:
            <span class="process-step-1">Select data</span>
            <span class="process-arrow">→</span>
            <span class="process-step-2">Choose columns</span>
            <span class="process-arrow">→</span>
            <span class="process-step-3">Compare clustering scores</span>
            <span class="process-arrow">→</span>
            <span class="process-step-4">Select K</span>
            <span class="process-arrow">→</span>
            <span class="process-step-5">Create clusters</span>
            <span class="process-arrow">→</span>
            <span class="process-step-6">Generate names</span>
            <span class="process-arrow">→</span>
            <span class="process-step-7">Download CSV</span>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.divider()
    st.subheader('Step 1: Choose a dataset | בחירת קובץ')

    sample_one, sample_two, sample_three = st.columns(3)

    with sample_one:
        st.info('Customers.csv\n\n2,000 customer records')

    with sample_two:
        st.info('ecommerce.csv\n\n350 e-commerce customers')

    with sample_three:
        st.info('iris_unlabaled.csv\n\n150 iris flower records')

    example_files = {
        'Upload my own CSV | העלאת קובץ אישי': None,
        'Customers.csv — 2,000 rows': 'Customers.csv',
        'ecommerce.csv — 350 rows': 'ecommerce.csv',
        'iris_unlabaled.csv — 150 rows': 'iris_unlabaled.csv'
    }

    data_source = st.selectbox(
        'Choose an example or upload your own file',
        list(example_files.keys())
    )

    selected_example = example_files[data_source]
    uploaded_file = None

    if selected_example is None:
        uploaded_file = st.file_uploader(
            'Drag and drop a CSV file here or click Browse files',
            type=['csv'],
            accept_multiple_files=False
        )

        if uploaded_file is None:
            return

        df = pd.read_csv(uploaded_file)
        current_file_name = uploaded_file.name
    else:
        df = pd.read_csv(selected_example)
        current_file_name = selected_example

    if st.session_state.get('active_file_name') != current_file_name:
        reset_results()
        st.session_state['active_file_name'] = current_file_name

    st.subheader('Data preview | תצוגת הנתונים')

    rows_column, columns_column, missing_column = st.columns(3)

    rows_column.metric('Rows', df.shape[0])
    columns_column.metric('Columns', df.shape[1])
    missing_column.metric('Missing values', int(df.isna().sum().sum()))

    show_styled_table(df)

    default_columns = []

    for column in df.columns:
        if (
            column not in ['CustomerID', 'Customer ID', 'target']
            and not str(column).startswith('Unnamed')
        ):
            default_columns.append(column)

    selected_columns = st.multiselect(
        'Select columns for clustering | בחירת עמודות',
        df.columns.tolist(),
        default=default_columns
    )

    selection_signature = current_file_name + '|' + '|'.join(selected_columns)

    if st.session_state.get('selection_signature') != selection_signature:
        clear_analysis_results()
        st.session_state['selection_signature'] = selection_signature

    if len(selected_columns) == 0:
        st.info('Select at least one column for clustering.')
        return

    data, encoded_data, df_scaled, numeric_columns, categorical_columns = (
        prepare_data(df, selected_columns)
    )

    if encoded_data.shape[1] == 0:
        st.error('The selected columns cannot be converted to numbers.')
        return

    largest_k = min(10, len(df) - 1)

    if largest_k < 2:
        st.error('The CSV file must contain at least three rows.')
        return

    st.divider()
    st.subheader(
        'Step 2: WCSS and Silhouette Score | השוואת מדדי האשכולות'
    )

    if (
        'min_k_input' not in st.session_state
        or st.session_state['min_k_input'] < 2
        or st.session_state['min_k_input'] > largest_k
    ):
        st.session_state['min_k_input'] = 2

    if (
        'max_k_input' not in st.session_state
        or st.session_state['max_k_input'] < 2
        or st.session_state['max_k_input'] > largest_k
    ):
        st.session_state['max_k_input'] = largest_k

    if st.session_state['min_k_input'] > st.session_state['max_k_input']:
        st.session_state['max_k_input'] = st.session_state['min_k_input']

    min_column, max_column = st.columns(2)

    with min_column:
        min_k = st.number_input(
            'Min K',
            min_value=2,
            max_value=largest_k,
            step=1,
            key='min_k_input',
            on_change=synchronize_min_k
        )

    with max_column:
        max_k = st.number_input(
            'Max K',
            min_value=2,
            max_value=largest_k,
            step=1,
            key='max_k_input',
            on_change=synchronize_max_k
        )

    if st.button('Calculate WCSS and Silhouette', type='primary'):
        st.session_state['score_table'] = calculate_clustering_scores(
            df_scaled,
            int(min_k),
            int(max_k)
        )
        st.session_state['score_columns'] = selected_columns.copy()

    if 'score_table' in st.session_state:
        score_table = st.session_state['score_table']
        st.info(
            'Columns used in this calculation: '
            + ', '.join(st.session_state['score_columns'])
        )
        show_styled_table(score_table)
        show_elbow_chart(score_table)
        show_silhouette_chart(score_table)

        best_k = select_best_k(score_table)
        best_score = score_table.loc[
            score_table['k'] == best_k,
            'Silhouette Score'
        ].iloc[0]

        st.success(
            f'Best Silhouette result: K = {best_k}, score = {best_score:.4f}'
        )

    st.divider()
    st.subheader('Step 3: Create clusters | יצירת אשכולות')

    if (
        'selected_k_input' not in st.session_state
        or st.session_state['selected_k_input'] < 2
        or st.session_state['selected_k_input'] > largest_k
    ):
        st.session_state['selected_k_input'] = min(3, largest_k)

    automatic_method = st.radio(
        'Automatic K method | שיטת בחירת K אוטומטית',
        ['Silhouette Score', 'WCSS with Ollama'],
        horizontal=True,
        key='automatic_k_method'
    )

    if 'score_table' in st.session_state:
        wcss_api_key = ''

        if automatic_method == 'WCSS with Ollama':
            wcss_api_key = st.text_input(
                'Ollama API key for automatic WCSS selection',
                type='password',
                key='wcss_api_key'
            )

        if st.button('Choose K automatically'):
            automatic_k = None

            if automatic_method == 'Silhouette Score':
                automatic_k = select_best_k(
                    st.session_state['score_table']
                )
                selection_message = (
                    f'K = {automatic_k} was selected because it has the '
                    'highest Silhouette Score.'
                )
            elif wcss_api_key == '':
                st.warning('Enter your Ollama API key for WCSS selection.')
            else:
                try:
                    with st.spinner('Ollama is choosing K from the WCSS values...'):
                        automatic_k = select_k_with_ollama(
                            st.session_state['score_table'],
                            wcss_api_key
                        )

                    selection_message = (
                        f'Ollama selected K = {automatic_k} from the WCSS '
                        'values and the Elbow Method.'
                    )
                except Exception:
                    st.error(
                        'Ollama did not return a valid K. Check the API key '
                        'and try again.'
                    )

            if automatic_k is not None:
                available_k_values = (
                    st.session_state['score_table']['k'].tolist()
                )

                if automatic_k in available_k_values:
                    clear_cluster_results()
                    st.session_state['selected_k_input'] = automatic_k
                    st.success(selection_message)
                else:
                    st.error(
                        'Ollama returned a K outside the calculated range.'
                    )
    else:
        st.button('Choose K automatically', disabled=True)
        st.caption(
            'Calculate WCSS and Silhouette scores before automatic selection.'
        )

    selected_k = st.number_input(
        'Select K',
        min_value=2,
        max_value=largest_k,
        step=1,
        key='selected_k_input',
        on_change=clear_cluster_results
    )

    remove_outliers_option = st.checkbox(
        'Remove outliers before final clustering | ניקוי חריגים',
        value=False,
        key='remove_outliers_input',
        on_change=clear_cluster_results
    )

    if remove_outliers_option:
        st.info(
            'Rows whose distance from their cluster center is more than two '
            'standard deviations above the average will be removed.'
        )

    if st.button('Create clusters', type='primary'):
        working_df = df.copy()
        working_data = data.copy()
        working_scaled_data = df_scaled.copy()
        removed_rows = 0
        outlier_threshold = 0

        if remove_outliers_option:
            (
                working_df,
                working_data,
                working_scaled_data,
                removed_rows,
                outlier_threshold
            ) = remove_outliers(
                df,
                data,
                df_scaled,
                int(selected_k)
            )

        if len(working_df) < int(selected_k):
            st.error('Too many rows were removed for the selected K.')
            return

        kmeans_model, cluster_labels = create_clusters(
            working_scaled_data,
            int(selected_k)
        )

        cluster_table = create_cluster_table(cluster_labels)
        cluster_summary = create_cluster_summary(
            working_data,
            cluster_labels,
            numeric_columns,
            categorical_columns,
            int(selected_k)
        )

        pca_data, pca_explained_variance = create_pca_data(
            working_scaled_data,
            cluster_labels
        )

        joblib.dump(kmeans_model, 'kmeans_model.pkl')

        st.session_state['cluster_labels'] = cluster_labels
        st.session_state['cluster_table'] = cluster_table
        st.session_state['cluster_summary'] = cluster_summary
        st.session_state['original_data'] = working_df.copy()
        st.session_state['original_file_name'] = current_file_name
        st.session_state['outlier_count'] = removed_rows
        st.session_state['outlier_threshold'] = outlier_threshold
        st.session_state['outlier_cleaning_used'] = remove_outliers_option
        st.session_state['original_row_count'] = len(df)
        st.session_state['cleaned_row_count'] = len(working_df)
        st.session_state['pca_data'] = pca_data
        st.session_state['pca_explained_variance'] = pca_explained_variance

    if 'cluster_table' not in st.session_state:
        return

    if st.session_state['outlier_cleaning_used']:
        removed_column, remaining_column, threshold_column = st.columns(3)
        removed_column.metric('Outliers removed', st.session_state['outlier_count'])
        remaining_column.metric(
            'Rows remaining',
            st.session_state['cleaned_row_count']
        )
        threshold_column.metric(
            'Distance threshold',
            f"{st.session_state['outlier_threshold']:.3f}"
        )
    else:
        st.info('Outlier removal was not selected for this clustering run.')

    st.write('Cluster table | טבלת האשכולות')
    show_styled_table(st.session_state['cluster_table'])

    st.write('Cluster summary | סיכום האשכולות')
    show_styled_table(st.session_state['cluster_summary'])

    st.write('PCA visualization | הצגת האשכולות בשני ממדים')

    if st.session_state['pca_data'] is None:
        st.info(
            'Select at least two encoded features to create a two-dimensional '
            'PCA visualization.'
        )
    else:
        st.info(
            'PCA reduces the selected features to two visual components. '
            'The colors represent the clusters created by K-Means.'
        )
        st.metric(
            'Variance represented by PC1 and PC2',
            f"{st.session_state['pca_explained_variance']:.2f}%"
        )
        show_pca_chart(st.session_state['pca_data'])

    st.divider()
    st.subheader('Step 4: Generate names with Ollama | יצירת שמות')

    api_key = st.text_input('Ollama API key', type='password')

    if st.button('Generate cluster names', type='primary'):
        if api_key == '':
            st.warning('Enter your Ollama API key.')
        else:
            with st.spinner('Ollama is naming the clusters...'):
                named_cluster_table = name_clusters(
                    st.session_state['cluster_summary'],
                    st.session_state['cluster_table'],
                    api_key
                )

            result_data = create_result_data(
                st.session_state['original_data'],
                st.session_state['cluster_labels'],
                named_cluster_table
            )

            st.session_state['cluster_table'] = named_cluster_table
            st.session_state['result_data'] = result_data

    if 'result_data' not in st.session_state:
        return

    st.success('The clusters were created successfully.')
    show_styled_table(st.session_state['cluster_table'])

    csv_data = st.session_state['result_data'].to_csv(
        index=False
    ).encode('utf-8-sig')

    original_name = st.session_state['original_file_name']
    output_name = original_name.rsplit('.', 1)[0] + '_clustered.csv'

    st.download_button(
        'Download clustered CSV',
        data=csv_data,
        file_name=output_name,
        mime='text/csv',
        type='primary'
    )


if __name__ == '__main__':
    main()
