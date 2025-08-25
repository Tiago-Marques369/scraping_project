from datetime import datetime
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from scraper.books_scraper import scrape_books_to_parquet

DAG_ID = "books_pipeline_dag"

with DAG(
    DAG_ID,
    description="Scrape BooksToScrape Science category -> Parquet -> dbt (DuckDB)",
    start_date=pendulum.datetime(2025, 8, 1, tz="America/Sao_Paulo"),
    schedule_interval="@daily",
    catchup=False,
    default_args={"retries": 1},
    tags=["books", "scraping", "dbt", "duckdb"],
) as dag:

    scrape = PythonOperator(
        task_id="scrape_books",
        python_callable=scrape_books_to_parquet,
        op_kwargs={
            "category_url": "https://books.toscrape.com/catalogue/category/books/science_22/index.html",
            "out_dir": "/opt/airflow/data/raw",
        },
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        cwd="/opt/airflow/dags/dbt/books_dbt",
        bash_command="dbt deps && dbt build --profiles-dir .",
    )

    scrape >> dbt_build