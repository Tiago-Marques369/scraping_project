
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select title
from "books"."main"."stg_books"
where title is null



  
  
      
    ) dbt_internal_test