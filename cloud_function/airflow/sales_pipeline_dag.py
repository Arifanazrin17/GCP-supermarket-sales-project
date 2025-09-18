from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.utils.dates import days_ago
from config import STAGING_TABLE, CURATED_TABLE

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="sales_pipeline_dag",
    default_args=default_args,
    description="Refresh curated sales table with partitions",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    create_partitioned = BigQueryInsertJobOperator(
        task_id="create_partitioned_table",
        configuration={
            "query": {
                "query": "{% include 'sql/create_partitioned.sql' %}",
                "useLegacySql": False,
                "destinationTable": {
                    "projectId": CURATED_TABLE.split(".")[0],
                    "datasetId": CURATED_TABLE.split(".")[1],
                    "tableId": CURATED_TABLE.split(".")[2],
                },
                "writeDisposition": "WRITE_TRUNCATE",
            }
        },
        params={"staging_table": STAGING_TABLE, "curated_table": CURATED_TABLE},
    )

    create_partitioned
