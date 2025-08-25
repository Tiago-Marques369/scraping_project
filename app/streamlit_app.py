import duckdb
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

DB_PATH = Path('data/warehouse/books.duckdb')

st.set_page_config(page_title="Books — Science Category", layout="wide")

st.title("BooksToScrape — Science (dbt + DuckDB)")

if not DB_PATH.exists():
    st.warning("Warehouse not found yet. Run the Airflow DAG first to populate DuckDB at data/warehouse/books.duckdb.")
else:
    con = duckdb.connect(str(DB_PATH))
    st.subheader("Raw (stg_books)")
    stg = con.execute("SELECT * FROM stg_books ORDER BY price_gbp DESC").df()
    st.dataframe(stg, use_container_width=True, hide_index=True)

    st.subheader("Preço por avaliação")
    fact = con.execute("SELECT * FROM fct_prices_by_rating").df()

    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.bar(fact, x="rating", y="n_books", color="rating", title="Qtd de livros por rating")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = px.line(fact, x="date_scraped", y="avg_price_gbp", color="rating", markers=True, title="Preço médio (GBP) por rating ao longo do tempo")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Top 10 mais caros")
    top10 = stg.sort_values("price_gbp", ascending=False).head(10)[["title","price_gbp","rating","availability","product_page"]]
    st.dataframe(top10, use_container_width=True, hide_index=True)
