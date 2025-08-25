# Books Pipeline Project

## Overview

This project demonstrates a complete data engineering workflow using **Airflow**, **dbt**, **DuckDB**, and **Streamlit**. The pipeline scrapes book data, transforms it with dbt, and provides a dashboard with Streamlit.

**Pipeline Steps:**

1. **Web Scraping**  
   - Scrapes book data from the Science category of [Books to Scrape](https://books.toscrape.com/catalogue/category/books/science_22/index.html).  
   - Handles encoding issues for prices (`£42.96` or `Â£42.96`).  
   - Saves data as **Parquet** files in `/opt/airflow/data/raw/`.

2. **ETL/Transformation with dbt**  
   - Uses **DuckDB** as a warehouse.  
   - Models and transforms raw Parquet data into structured tables.  
   - Stores the DuckDB database in `/opt/airflow/data/warehouse/books.duckdb`.  
   - Ensure the folder `data/warehouse` exists before running dbt.

3. **Dashboard with Streamlit**  
   - Reads the DuckDB database and visualizes metrics such as average price, availability, and rating distributions.  

---

## Architecture

```
[ Books to Scrape Website ]
           │
           ▼
      Web Scraper
   (Airflow PythonOperator)
           │
           ▼
  Parquet files in /data/raw
           │
           ▼
         dbt Build
   (Airflow BashOperator)
           │
           ▼
DuckDB Warehouse (/data/warehouse)
           │
           ▼
     Streamlit Dashboard
```

---

## Airflow DAG

- DAG name: `books_pipeline_dag`  
- Tasks:
  1. `scrape_books` – Scrape and save data as Parquet.
  2. `dbt_build` – Run dbt models on DuckDB.  

**Trigger DAG manually or via schedule in Airflow UI.**

---

## Setup Instructions

1. **Create directories**:

```bash
mkdir -p data/raw data/warehouse
```

2. **Install dependencies** (inside Airflow container):

```bash
pip install -r requirements.txt
```

3. **Run Airflow**:

```bash
docker-compose up -d
```

4. **Clear and trigger DAG**:

- In Airflow UI: DAG → Clear Tasks → Trigger DAG  
- Or via terminal:

```bash
docker exec -it <scheduler_container_id> \
airflow tasks clear books_pipeline_dag --yes
docker exec -it <scheduler_container_id> \
airflow dags trigger books_pipeline_dag
```

5. **Check logs**:

- Scraper output:

```
[scraper] wrote parquet: /opt/airflow/data/raw/books_YYYY-MM-DD.parquet with N rows
```

- dbt output: verifies creation of DuckDB database at `/opt/airflow/data/warehouse/books.duckdb`.

---

## Notes

- `_parse_price` function in the scraper now removes unexpected characters to avoid conversion errors.  
- Ensure `data/warehouse` exists to allow dbt to create `books.duckdb`.  
- Streamlit reads the DuckDB database for visualization.

