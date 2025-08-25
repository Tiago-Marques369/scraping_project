WITH src AS (
  SELECT * FROM read_parquet('/opt/airflow/data/raw/*.parquet')
)
SELECT
  date_scraped::DATE as date_scraped,
  title,
  product_page,
  price_gbp,
  availability,
  rating,
  category
FROM src