
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select date_scraped
from "books"."main"."stg_books"
where date_scraped is null



  
  
      
    ) dbt_internal_test