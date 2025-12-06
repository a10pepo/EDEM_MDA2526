
  
    

  create  table "pruebadb"."public"."int_valenbisi__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    number,
    address,
    lat,
    lon,
    available,
    free,
    total,
    ROUND((total - free)::numeric / total * 100, 2) AS occupancy_pct,
    open,
    updated_at,
    update_jcd
FROM "pruebadb"."public"."stg_valenbisi"
  );
  