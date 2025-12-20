-- Enriquece clientes: normaliza email, separa nombre en dos columnas cuando sea posible y calcula edad aproximada (años).

with c as (

    select * from "dev"."main"."stg_customers"

),

enriched as (

    select
        customer_id,
        customer_name,
        -- intento simple de split: parte antes del primer espacio como first_name
        case
            when position(' ' in customer_name) > 0 then split_part(customer_name, ' ', 1)
            else customer_name
        end as first_name,
        case
            when position(' ' in customer_name) > 0 then
                ltrim(substr(customer_name, length(split_part(customer_name, ' ', 1)) + 1))
            else null
        end as last_name,
        email,
        telephone,
        city,
        country,
        gender,
        job_title,
        date_of_birth,
        -- edad aproximada en años (año actual - año nacimiento)
        cast(strftime('%Y', current_date) as integer) - cast(strftime('%Y', date_of_birth) as integer) as age
    from c
)

select * from enriched