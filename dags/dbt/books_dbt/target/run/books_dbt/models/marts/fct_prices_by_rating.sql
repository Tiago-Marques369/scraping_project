
  
    
    

    create  table
      "books"."main"."fct_prices_by_rating__dbt_tmp"
  
    as (
      SELECT
  date_scraped,
  rating,
  COUNT(*) AS n_books,
  AVG(price_gbp) AS avg_price_gbp,
  MIN(price_gbp) AS min_price_gbp,
  MAX(price_gbp) AS max_price_gbp
FROM "books"."main"."stg_books"
GROUP BY 1,2
ORDER BY 1,2
    );
  
  