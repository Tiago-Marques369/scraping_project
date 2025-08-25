# Books Data Pipeline — Airflow + dbt (DuckDB) + Streamlit

End-to-end pipeline: scrape book data, transform with dbt on DuckDB, and explore via Streamlit. This README reflects the **actual repository layout** used in this project.

---

## Tech Stack
- **Apache Airflow** (LocalExecutor) for orchestration
- **Python** (Requests, BeautifulSoup, Pandas, PyArrow) for scraping/ingest
- **DuckDB** as the local warehouse
- **dbt-duckdb** for SQL transformations
- **Streamlit** for the dashboard
- **Docker Compose** for local infra

---

## Folder Structure (as shipped)
```
.
├── app/
│   ├── requirements.txt
│   └── streamlit_app.py
├── dags/
│   ├── books_pipeline_dag.py
│   ├── dbt/
│   │   └── books_dbt/
│   │       ├── dbt_project.yml
│   │       ├── profiles.yml
│   │       └── models/
│   │           ├── staging/
│   │           │   ├── schema.yml
│   │           │   └── stg_books.sql
│   │           └── marts/
│   │               └── fct_prices_by_rating.sql
│   └── scraper/
│       └── books_scraper.py
├── data/
│   ├── raw/
│   └── warehouse/
├── docker-compose.yml
├── logs/
└── requirements.txt
```

**Notes**
- `requirements.txt` (root) is installed in the Airflow image via `_PIP_ADDITIONAL_REQUIREMENTS`.
- `app/requirements.txt` is used by the Streamlit service/container.
- `data/` is a bind mount so files are visible to you on the host.

---

## How It Works (short)
1. **Scrape (PythonOperator)**: requests + BeautifulSoup parse the Science category pages; robust price parsing to handle encoding oddities (e.g., `Â£42.96`). Output: **Parquet** in `data/raw/`.
2. **Transform (dbt + DuckDB)**: dbt models read Parquet and materialize into `data/warehouse/books.duckdb`:
   - `stg_books` (table)
   - `fct_prices_by_rating` (table)
3. **Visualize (Streamlit)**: reads from `data/warehouse/books.duckdb` and shows tables/aggregations.

---

## Quickstart (Docker)

### 1) Clone and enter
```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2) Create required folders (first run)
```bash
mkdir -p data/raw data/warehouse
```

### 3) Start services
```bash
docker compose up -d
```

- Airflow: http://localhost:8080 (login: `admin` / `admin`)
- Streamlit: http://localhost:8501

### 4) Run the DAG
- In Airflow UI → unpause **`books_pipeline_dag`**
- Trigger the DAG
- Check logs:
  - Scraper: `"[scraper] wrote parquet: /opt/airflow/data/raw/books_YYYY-MM-DD.parquet with N rows"`
  - dbt: successful build and creation of `data/warehouse/books.duckdb`

### 5) Open the dashboard
- http://localhost:8501

---

## Components

### Scraper (Python)
- File: `dags/scraper/books_scraper.py`
- Key behavior:
  - Iterates through pagination; extracts `title`, `product_page`, `price_gbp`, `availability`, `rating`
  - Robust `_parse_price` strips non-numeric chars to avoid float errors
  - Writes daily Parquet snapshot into `data/raw/`

### Airflow DAG
- File: `dags/books_pipeline_dag.py`
- Tasks:
  1) `scrape_books` → PythonOperator
  2) `dbt_build` → BashOperator: `dbt deps && dbt build --profiles-dir .`
- Default schedule: `@daily` (change as you wish)

### dbt Project
- Location: `dags/dbt/books_dbt`
- Run inside container (path is the same inside Airflow):
  ```bash
  cd /opt/airflow/dags/dbt/books_dbt
  dbt deps && dbt build --profiles-dir .
  ```
- `profiles.yml` points to `/opt/airflow/data/warehouse/books.duckdb`
- Models:
  - `stg_books.sql` (staging)
  - `fct_prices_by_rating.sql` (mart)
  - Data tests in `staging/schema.yml`

### Streamlit App
- File: `app/streamlit_app.py`
- Reads DuckDB from `../data/warehouse/books.duckdb`
- Start is handled by `docker-compose`; to run locally:
  ```bash
  cd app
  pip install -r requirements.txt
  streamlit run streamlit_app.py
  ```

---

## Troubleshooting

**dbt IO Error: cannot open `/opt/.../data/warehouse/books.duckdb`**
- Ensure folder exists before building:
  ```bash
  mkdir -p data/warehouse
  ```
- Clear `dbt_build` task and trigger DAG again.

**Scraper ValueError on price (e.g., `'Â42.96'`)**
- Already handled by `_parse_price`. Make sure your code matches this repo’s version.

**DAG not showing in UI**
- Confirm volume mounts in `docker-compose.yml`:
  ```yaml
  - ./dags:/opt/airflow/dags
  - ./data:/opt/airflow/data
  ```
- Restart:
  ```bash
  docker compose down && docker compose up -d
  ```

**Verify outputs**
```bash
ls -lh data/raw/
ls -lh data/warehouse/
```

---

## Extend
- Enrich with product detail pages (dimensions).
- Partition by category and date; snapshot strategy.
- Add CI for `dbt build` + tests.
- Swap DuckDB for a cloud warehouse (BigQuery, Snowflake, etc.).
- Containerize Streamlit as an independent service.

---

## Attribution & License
- Dataset: public demo site **Books to Scrape** (educational use).  
- You may use/modify this project for learning and portfolio. Attribution appreciated.
