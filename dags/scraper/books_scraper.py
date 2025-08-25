from __future__ import annotations
import os, re
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timezone
import pyarrow as pa
import pyarrow.parquet as pq

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DataEngineerBot/1.0; +https://example.com)"
}

def _rating_to_int(classes):
    # ratings são dados via classes como "star-rating Three"
    mapping = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
    for c in classes:
        if c in mapping:
            return mapping[c]
    return None

def _parse_price(pounds_text: str) -> float:
    # Limpa caracteres estranhos e moeda, mantém só números/ponto
    cleaned = re.sub(r"[^0-9.]", "", pounds_text)
    return float(cleaned) if cleaned else None

def _fetch(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text

def _parse_page(html: str, base_url: str):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for art in soup.select("article.product_pod"):
        title = art.h3.a.get("title")
        product_rel = art.h3.a.get("href")
        product_page = urljoin(base_url, product_rel)

        price = _parse_price(art.select_one("p.price_color").text)
        availability_text = art.select_one("p.instock.availability").get_text(strip=True)
        # Ex: "In stock (22 available)"
        avail_num = None
        m = re.search(r"(\\d+)", availability_text)
        if m:
            avail_num = int(m.group(1))

        rating = _rating_to_int(art.select_one("p.star-rating")["class"])

        items.append({
            "title": title,
            "product_page": product_page,
            "price_gbp": price,
            "availability": avail_num,
            "rating": rating,
        })

    # Próxima página
    next_li = soup.select_one("li.next a")
    next_url = urljoin(base_url, next_li["href"]) if next_li else None

    return items, next_url

def scrape_books(category_url: str) -> pd.DataFrame:
    cur = category_url
    base = "{uri.scheme}://{uri.netloc}/".format(uri=urlparse(category_url))
    all_rows = []
    while cur:
        html = _fetch(cur)
        rows, next_url = _parse_page(html, cur)
        all_rows.extend(rows)
        cur = next_url
    df = pd.DataFrame(all_rows)
    now = datetime.now(timezone.utc).astimezone()
    df["date_scraped"] = now.date().isoformat()
    df["category"] = "Science"
    # Enforce tipos
    df["price_gbp"] = pd.to_numeric(df["price_gbp"], errors="coerce")
    df["availability"] = pd.to_numeric(df["availability"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    return df

def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def scrape_books_to_parquet(category_url: str, out_dir: str) -> str:
    _ensure_dir(out_dir)
    df = scrape_books(category_url)
    out_path = os.path.join(out_dir, f"books_{df['date_scraped'].iloc[0]}.parquet")
    table = pa.Table.from_pandas(df)
    pq.write_table(table, out_path)
    print(f"[scraper] wrote parquet: {out_path} com {len(df)} linhas")
    return out_path

if __name__ == "__main__":
    # teste rápido fora do Airflow
    p = scrape_books_to_parquet(
        "https://books.toscrape.com/catalogue/category/books/science_22/index.html",
        "./data/raw"
    )
    print("wrote:", p)
