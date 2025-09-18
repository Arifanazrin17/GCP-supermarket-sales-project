import os
from google.cloud import bigquery, storage

# Environment variable: set BQ_TABLE in Cloud Function settings
BQ_TABLE = os.environ.get(
    "BQ_TABLE",
    "acoustic-apex-469415-m0.Freshmart_branch_daily_sales.freshmart_sales_data"
)

def gcs_to_bq(event, context):
    """
    Triggered when a file is uploaded to Cloud Storage.
    Only processes CSVs under Store-data/ folder.
    Loads them into BigQuery.
    """

    bucket_name = event['bucket']
    file_name = event['name']  # e.g. "Store-data/sample_data_1.csv"
    print(f"Processing file: {file_name} from bucket: {bucket_name}")

    # Process only files under "Store-data/" and ending with .csv
    if not (file_name.startswith("Store-data/") and file_name.endswith(".csv")):
        print(f" Skipping file {file_name} (not a CSV in Store-data/ folder)")
        return

    storage_client = storage.Client()
    bq_client = bigquery.Client()

    # Download file locally
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    local_path = f"/tmp/{os.path.basename(file_name)}"
    blob.download_to_filename(local_path)

    # Configure load job
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_APPEND"  # Append new rows
    )

    # Load CSV into BigQuery
    with open(local_path, "rb") as source_file:
        load_job = bq_client.load_table_from_file(
            source_file,
            BQ_TABLE,
            job_config=job_config
        )

    load_job.result()  # Wait until complete

    print(f"Loaded {file_name} into {BQ_TABLE} with {load_job.output_rows} rows")
