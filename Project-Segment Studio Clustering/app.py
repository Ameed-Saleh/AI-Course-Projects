import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


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


def calculate_wcss(df_scaled, min_k, max_k):
    k_values = range(min_k, max_k + 1)
    wcss_values = []

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(df_scaled)
        wcss_values.append(kmeans.inertia_)

    wcss_table = pd.DataFrame({
        'k': list(k_values),
        'WCSS': wcss_values
    })

    return wcss_table


def create_clusters(df_scaled, selected_k):
    kmeans_model = KMeans(
        n_clusters=selected_k,
        random_state=42,
        n_init=10
    )

    kmeans_model.fit(df_scaled)
    cluster_labels = kmeans_model.labels_

    return kmeans_model, cluster_labels


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


def clear_cluster_results():
    cluster_keys = [
        'cluster_labels',
        'cluster_table',
        'cluster_summary',
        'original_data',
        'original_file_name',
        'result_data'
    ]

    for key in cluster_keys:
        if key in st.session_state:
            del st.session_state[key]


def clear_analysis_results():
    analysis_keys = ['wcss_table', 'wcss_columns']

    for key in analysis_keys:
        if key in st.session_state:
            del st.session_state[key]

    clear_cluster_results()


def reset_results():
    clear_analysis_results()

    control_keys = [
        'min_k_input',
        'max_k_input',
        'selected_k_input'
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
            <span class="process-step-3">Calculate WCSS</span>
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

    largest_k = min(10, len(df))

    if largest_k < 2:
        st.error('The CSV file must contain at least two rows.')
        return

    st.divider()
    st.subheader('Step 2: WCSS and Elbow Method | בחירת טווח K')

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

    if st.button('Calculate WCSS', type='primary'):
        st.session_state['wcss_table'] = calculate_wcss(
            df_scaled,
            int(min_k),
            int(max_k)
        )
        st.session_state['wcss_columns'] = selected_columns.copy()

    if 'wcss_table' in st.session_state:
        wcss_table = st.session_state['wcss_table']
        st.info(
            'Columns used in this calculation: '
            + ', '.join(st.session_state['wcss_columns'])
        )
        show_styled_table(wcss_table)
        show_elbow_chart(wcss_table)

    st.divider()
    st.subheader('Step 3: Create clusters | יצירת אשכולות')

    selected_k = st.number_input(
        'Select K',
        min_value=2,
        max_value=largest_k,
        value=min(3, largest_k),
        step=1,
        key='selected_k_input',
        on_change=clear_cluster_results
    )

    if st.button('Create clusters', type='primary'):
        kmeans_model, cluster_labels = create_clusters(
            df_scaled,
            int(selected_k)
        )

        cluster_table = create_cluster_table(cluster_labels)
        cluster_summary = create_cluster_summary(
            data,
            cluster_labels,
            numeric_columns,
            categorical_columns,
            int(selected_k)
        )

        joblib.dump(kmeans_model, 'kmeans_model.pkl')

        st.session_state['cluster_labels'] = cluster_labels
        st.session_state['cluster_table'] = cluster_table
        st.session_state['cluster_summary'] = cluster_summary
        st.session_state['original_data'] = df.copy()
        st.session_state['original_file_name'] = current_file_name

    if 'cluster_table' not in st.session_state:
        return

    st.write('Cluster table | טבלת האשכולות')
    show_styled_table(st.session_state['cluster_table'])

    st.write('Cluster summary | סיכום האשכולות')
    show_styled_table(st.session_state['cluster_summary'])

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
