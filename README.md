# Books Scraping Pipeline with Airflow, dbt, and Streamlit

## Overview
This project demonstrates an end-to-end data pipeline for scraping, transforming, and visualizing book data.  
The workflow is orchestrated with **Apache Airflow**, transformations are applied using **dbt**, storage is managed with **DuckDB**, and an interactive **Streamlit** dashboard allows data exploration.

---

## Architecture
1. **Web Scraping** – Extracts book data (title, price, rating, availability) from [Books to Scrape](https://books.toscrape.com/catalogue/category/books/science_22/index.html).  
2. **Airflow Orchestration** – Automates scraping tasks, manages scheduling, and monitors execution.  
3. **Storage** – Saves raw and transformed data into **DuckDB** and Parquet files.  
4. **dbt Modeling** – Transforms and cleans raw data into analysis-ready models.  
5. **Streamlit Dashboard** – Provides an interactive visualization of book insights.  

---

## Tech Stack
- **Apache Airflow** – Orchestration and scheduling  
- **Python** – Web scraping and ETL (Requests, BeautifulSoup, Pandas)  
- **DuckDB** – Local analytical storage  
- **dbt** – Data transformations  
- **Streamlit** – Dashboard and visualization  
- **Docker** – Containerized environment  

---

## Project Structure
```
.
├── dags/
│   ├── books_pipeline_dag.py        # Airflow DAG
│   └── scraper/books_scraper.py     # Scraping logic
├── dbt/
│   └── models/                      # dbt models
├── streamlit_app/
│   └── app.py                       # Dashboard code
├── data/                            # DuckDB and Parquet outputs
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Step-by-Step Setup

### 1. Clone the repository
```bash
git clone <your_repo_url>
cd <your_repo_folder>
```

### 2. Start Docker containers
```bash
docker-compose up -d
```

This will launch Airflow webserver, scheduler, and a Postgres metadata database.

### 3. Access Airflow
Go to [http://localhost:8080](http://localhost:8080)  
- Username: `airflow`  
- Password: `airflow`  

Activate the **`books_pipeline_dag`** and trigger it.

### 4. Run dbt transformations
Inside the container or locally (if dbt is installed):
```bash
cd dbt
dbt run
```

This will create clean models inside DuckDB.

### 5. Launch Streamlit dashboard
```bash
cd streamlit_app
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) to explore the dashboard.

---

## Results
- **Raw Data**: Scraped book data stored in Parquet/DuckDB.  
- **Transformed Data**: Clean tables created with dbt models.  
- **Dashboard**: Streamlit app showing prices, ratings distribution, and availability.  

---

## Next Steps
- Extend scraping to multiple categories.  
- Automate dbt runs directly from Airflow.  
- Deploy Streamlit dashboard on cloud (e.g., Streamlit Cloud or AWS ECS).  
