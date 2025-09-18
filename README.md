# GCP-supermarket-sales-project
🏗️ GCP Architecture

1. Data Sources (Supermarket Transactions)
Simulated POS system generates sales data (CSV/JSON files, or streaming events like Pub/Sub).
Two types of data:
Transactional data → product sales,  stores
2. Ingestion Layer
*Batch Ingestion*: Upload daily CSV/JSON sales files → Cloud Storage (GCS) (Raw zone).
*Streaming Ingestion*: Real-time sales messages → Pub/Sub.
3. Processing Layer
*Cloud Functions* (triggered by GCS upload):
  -Validate & clean CSV.
  -Load into BigQuery staging tables.
*Dataflow (Apache Beam)* → transforms raw data from Pub/Sub → write into BigQuery (streaming pipeline).
BigQuery → ELT transformations (SQL-based modeling).
4. Orchestration
*Cloud Composer (Airflow)* → schedule:
Move data from GCS → BigQuery
Trigger Dataflow jobs
Run validation checks
Refresh Looker dashboards
5. Data Warehouse / Analytics Layer
*BigQuery* → main analytical data warehouse.
Create fact tables (sales, payments) and dimension tables (products, customers, stores).
Build star schema for reporting.
6. Visualization
*Looker Studio* / Looker → dashboards:
Daily Sales Trend
Top 10 Products by Revenue
Store Performance Comparison
Customer Segmentation
7. Monitoring & Governance (**pipeline in future)
Cloud Monitoring / Logging → monitor pipeline health.
IAM → restrict access (e.g., analysts can only query curated datasets).
Data Catalog → document datasets.
-----------------------------------------------------------------------------------------------------------
This project will help you practice:  
Data ingestion (batch + streaming)  
Data storage (raw vs. curated)  
Data transformation (ETL/ELT pipelines)  
Orchestration (Airflow)  
Data modeling &amp; analytics (BigQuery, Looker)  
Monitoring &amp; security (IAM, Logging, Monitoring) **planned in future
-----------------------------------------------------------------------------------------------------------
