
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    product_page as unique_field,
    count(*) as n_records

from "books"."main"."stg_books"
where product_page is not null
group by product_page
having count(*) > 1



  
  
      
    ) dbt_internal_test