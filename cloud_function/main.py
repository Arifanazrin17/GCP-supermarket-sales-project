import os
import csv
from datetime import datetime
from google.cloud import bigquery, storage
from config import BUCKET, RAW_PATH, STAGING_TABLE

def gcs_to_bq(event, context):
    """
    Triggered when a file is uploaded to GCS (daily_reports/).
    Validates CSV, cleans data, and loads into BigQuery staging table.
    """

    bucket_name = event.get("bucket")
    file_name = event.get("name")

    print(f"Processing file: gs://{bucket_name}/{file_name}")

    # Only process files inside daily_reports/ and CSVs
    if not (file_name.startswith(RAW_PATH) and file_name.lower().endswith(".csv")):
        print(f"Skipping file: {file_name}")
        return

    storage_client = storage.Client()
    bq_client = bigquery.Client()

    # Download raw file from GCS to /tmp
    local_raw = f"/tmp/{os.path.basename(file_name)}"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(local_raw)

    # Define required schema
    required_cols = [
        "sales_date","store_id","location",
        "product_id","product_name","category",
        "quantity_sold","unit_price","total_sales_amount"
    ]

    # Validate & clean
    local_clean = f"/tmp/cleaned_{os.path.basename(file_name)}"
    with open(local_raw, "r") as infile, open(local_clean, "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=required_cols)
        writer.writeheader()

        for row in reader:
            # Skip rows with missing values
            if any(row.get(c, "").strip() == "" for c in required_cols):
                continue

            # Validate date format
            try:
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                    try:
                        datetime.strptime(row["sales_date"], fmt)
                        break
                    except ValueError:
                        continue
                else:
                    raise ValueError("Invalid date format")
            except Exception:
                continue

            # Validate numeric fields
            try:
                int(row["quantity_sold"])
                float(row["unit_price"])
                float(row["total_sales_amount"])
            except ValueError:
                continue

            writer.writerow(row)

    # Load into BigQuery staging table
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    with open(local_clean, "rb") as source_file:
        load_job = bq_client.load_table_from_file(source_file, STAGING_TABLE, job_config=job_config)

    load_job.result()
    print(f"Loaded {file_name} into {STAGING_TABLE} with {load_job.output_rows} rows")
