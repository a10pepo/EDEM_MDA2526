with

supplies as (

    select * from {{ ref('staging__supplies') }}

)

select * from supplies
