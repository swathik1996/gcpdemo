from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.operators.pubsub import PubSubPullOperator
from airflow.providers.google.cloud.operators.gcs import GCSToLocalFilesystemOperator
from airflow.providers.google.cloud.operators.spanner import SpannerUpdateDatabaseOperator
from airflow.utils.dates import days_ago
import csv
 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}
 
dag = DAG(
    'gcs_to_spanner_dag',
    default_args=default_args,
    description='DAG to load file from GCS to Spanner',
    schedule_interval='@once',
    start_date=days_ago(1),
    tags=['example'],
)
 
start_task = DummyOperator(task_id='start', dag=dag)
 
pull_message_task = PubSubPullOperator(
    task_id='pull_message',
    project='your_project_id',
    subscription='your_pubsub_subscription',
    messages_num=1,
    return_immediately=True,
    ack_messages=True,
    dag=dag,
)
 
pull_file_task = GCSToLocalFilesystemOperator(
    task_id='pull_file_from_gcs',
    bucket='your_gcs_bucket',
    object='user-details.csv',
    filename='/tmp/user-details.csv',
    dag=dag,
)
 
def process_file(**kwargs):
    file_path = kwargs['ti'].xcom_pull(task_ids='pull_file_from_gcs')['output_path']
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        data_to_load = [row for row in reader]
    return data_to_load
 
process_file_task = PythonOperator(
    task_id='process_file',
    python_callable=process_file,
    provide_context=True,
    dag=dag,
)
 
load_to_spanner_task = SpannerUpdateDatabaseOperator(
    task_id='load_to_spanner',
    instance_id='your_spanner_instance',
    database_id='your_spanner_database',
    sql='INSERT INTO user_details (username, firstname, lastname, displayname, jobtitle, department) VALUES (%s, %s, %s, %s, %s, %s)',
    parameters="{{ task_instance.xcom_pull(task_ids='process_file') }}",
    dag=dag,
)
 
start_task >> pull_message_task >> pull_file_task >> process_file_task >> load_to_spanner_task
