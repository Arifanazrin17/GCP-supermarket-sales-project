-- Create partitioned curated sales table with derived date parts
CREATE OR REPLACE TABLE `{{ params.curated_table }}`
PARTITION BY DATE(sales_date) AS
SELECT 
    sales_date,
    store_id,
    location,
    product_id,
    product_name,
    category,
    quantity_sold,
    unit_price,
    total_sales_amount,
    EXTRACT(YEAR FROM sales_date) AS sales_year,
    EXTRACT(MONTH FROM sales_date) AS sales_month,
    EXTRACT(DAY FROM sales_date) AS sales_day
FROM `{{ params.staging_table }}`;
