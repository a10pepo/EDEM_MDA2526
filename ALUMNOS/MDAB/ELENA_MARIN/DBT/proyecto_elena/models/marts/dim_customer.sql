select
    customer_id,
    first_name,
    last_name,
    customer_name,
    email,
    telephone,
    city,
    country,
    gender,
    job_title,
    date_of_birth,
    age
from {{ ref('int_customers_clean') }}
