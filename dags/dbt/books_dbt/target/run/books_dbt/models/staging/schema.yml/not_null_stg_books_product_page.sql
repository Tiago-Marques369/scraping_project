
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select product_page
from "books"."main"."stg_books"
where product_page is null



  
  
      
    ) dbt_internal_test