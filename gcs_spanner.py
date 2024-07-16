from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator
from airflow.providers.google.cloud.operators.spanner import CloudSpannerInstanceDatabaseQueryOperator
from airflow.operators.python_operator import PythonOperator
from google.cloud import spanner

import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'gcs_to_spanner',
    default_args=default_args,
    description='A simple DAG to transfer data from GCS to Spanner',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

def process_and_upload_to_spanner(*args, **kwargs):
    # Assuming the file is a CSV for this example
    file_path = kwargs['ti'].xcom_pull(task_ids='download_from_gcs')

    # Read the file
    df = pd.read_csv(file_path)

    # Initialize Spanner client
    spanner_client = spanner.Client()
    instance = spanner_client.instance('your-instance-id')
    database = instance.database('your-database-id')

    # Process data and upload to Spanner
    with database.batch() as batch:
        for _, row in df.iterrows():
            batch.insert(
                table='your_table',
                columns=('column1', 'column2', 'column3'),
                values=[(row['column1'], row['column2'], row['column3'])],
            )

download_from_gcs = GCSToLocalFilesystemOperator(
    task_id='download_from_gcs',
    bucket='your-gcs-bucket',
    object_name='path/to/your/file.csv',
    filename='/tmp/file.csv',
    dag=dag,
)

upload_to_spanner = PythonOperator(
    task_id='upload_to_spanner',
    python_callable=process_and_upload_to_spanner,
    provide_context=True,
    dag=dag,
)

download_from_gcs >> upload_to_spanner
