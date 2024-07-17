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




from datetime import datetime
import time
from google.cloud import storage, spanner
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.google.cloud.operators.pubsub import (
    PubSubCreateSubscriptionOperator,
    PubSubPullOperator,
)
from airflow import XComArg

# Configuration variables
PROJECT_ID = "<PROJECT_ID>"
TOPIC_ID = "dag-topic-trigger"
SUBSCRIPTION = "trigger_dag_subscription"
GCS_BUCKET = "<GCS_BUCKET>"
GCS_OBJECT = "<GCS_OBJECT>"
SPANNER_INSTANCE_ID = "<SPANNER_INSTANCE_ID>"
SPANNER_DATABASE_ID = "<SPANNER_DATABASE_ID>"
SPANNER_TABLE = "<SPANNER_TABLE>"

# Custom functions
def download_gcs_file(bucket_name, object_name, local_file_path):
    """Download a file from GCS to local."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.download_to_filename(local_file_path)
    print(f"Downloaded {object_name} from bucket {bucket_name} to {local_file_path}")

def insert_data_into_spanner(local_file_path, instance_id, database_id, table):
    """Insert data into Spanner from a local file."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with open(local_file_path, 'r') as file:
        # Assuming the file contains CSV data
        rows = [line.strip().split(',') for line in file.readlines()]

    with database.batch() as batch:
        batch.insert(
            table=table,
            columns=('column1', 'column2', 'column3'),  # Adjust based on your table schema
            values=rows,
        )
    print(f"Inserted data from {local_file_path} into Spanner table {table}")

def transfer_data_from_gcs_to_spanner():
    local_file_path = '/tmp/temp_data.csv'  # Temporary local file path
    download_gcs_file(GCS_BUCKET, GCS_OBJECT, local_file_path)
    insert_data_into_spanner(local_file_path, SPANNER_INSTANCE_ID, SPANNER_DATABASE_ID, SPANNER_TABLE)
    print("Data transfer from GCS to Spanner completed.")

def handle_messages(pulled_messages, context):
    dag_ids = list()
    for idx, m in enumerate(pulled_messages):
        data = m.message.data.decode("utf-8")
        print(f"message {idx} data is {data}")
        dag_ids.append(data)
    return dag_ids

# This DAG will run minutely and handle pub/sub messages by triggering target DAG
with DAG(
    "trigger_dag",
    start_date=datetime(2021, 1, 1),
    schedule_interval="* * * * *",
    max_active_runs=1,
    catchup=False,
) as trigger_dag:
    # If subscription exists, we will use it. If not - create new one
    subscribe_task = PubSubCreateSubscriptionOperator(
        task_id="subscribe_task",
        project_id=PROJECT_ID,
        topic=TOPIC_ID,
        subscription=SUBSCRIPTION,
    )

    subscription = subscribe_task.output

    # Proceed maximum 50 messages in callback function handle_messages
    pull_messages_operator = PubSubPullOperator(
        task_id="pull_messages_operator",
        project_id=PROJECT_ID,
        ack_messages=True,
        messages_callback=handle_messages,
        subscription=subscription,
        max_messages=50,
    )

    # Trigger the data transfer DAG according to messages content
    trigger_target_dag = TriggerDagRunOperator.partial(task_id="trigger_target").expand(
        trigger_dag_id=XComArg(pull_messages_operator)
    )

    (subscribe_task >> pull_messages_operator >> trigger_target_dag)

# Simple DAG for transferring data from Google Cloud Storage to Spanner
with DAG(
    "transfer_data_to_spanner",
    start_date=datetime(2022, 1, 1),
    schedule_interval=None,
    catchup=False,
) as transfer_dag:
    transfer_task = PythonOperator(
        task_id="transfer_data_from_gcs_to_spanner",
        python_callable=transfer_data_from_gcs_to_spanner
    )

    transfer_task
