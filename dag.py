from airflow import DAG
from airflow.providers.google.cloud.operators.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGCSOperator
from airflow.providers.google.cloud.transfers.bigquery_to_mysql import BigQueryToMySqlOperator
from airflow.utils.dates import days_ago
from airflow.providers.google.common.hooks.base_google import GoogleBaseHook
from airflow.providers.google.cloud.transfers.gcs_to_mysql import GCSToMySqlOperator

value = element(split("-", var.cluster_id), length(split("-", var.cluster_id)) - 1)
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    dag_id='gcs_to_cloudsql',
    default_args=default_args,
    description='Load data from GCS to Cloud SQL',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Task: Load data from GCS to Cloud SQL
    load_gcs_to_cloudsql = GCSToMySqlOperator(
        task_id='load_gcs_to_cloudsql',
        bucket_name='your-gcs-bucket-name',
        source_objects=['path/to/your/file.csv'],
        schema_fields=[
            {'name': 'field1', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'field2', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            # Add schema fields as per your data
        ],
        destination_project_dataset_table='your_project_id.your_dataset.your_table',
        google_cloud_storage_conn_id='google_cloud_default',
        mysql_conn_id='cloud_sql_default',
        write_disposition='WRITE_TRUNCATE',
    )

    def process_file(**kwargs):
    file_path = kwargs['ti'].xcom_pull(task_ids='pull_file_from_gcs')['output_path']
    
    data_to_load = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            username, firstname, lastname, displayname, jobtitle, department = row
            data_to_load.append((username, firstname, lastname, displayname, jobtitle, department))
    
    return data_to_load

    load_gcs_to_cloudsql

