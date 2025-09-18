# GCP Project and Resources

PROJECT_ID = "acoustic-apex-469415-m0"

# Cloud Storage
BUCKET = "glsupermarket_sales_bucket"
RAW_PATH = "daily_reports/"     # raw csv files
FUNCTION_PATH = "cloudfunction" # where Cloud Function source code is stored

# BigQuery tables
STAGING_TABLE = f"{PROJECT_ID}.GLSupermarket_record.staging_sales_data"
CURATED_TABLE = f"{PROJECT_ID}.GLSupermarket_record.sales_partitioned"

# Cloud Function
CLOUD_FUNCTION = "gcs_to_bq"
