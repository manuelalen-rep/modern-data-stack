{{ config(materialized='view') }}

WITH source_data AS (
    SELECT * FROM {{ source('sap_data', 'zt_prod_clothing') }}
)

SELECT
    *,
    CASE 
        WHEN actual_time_min < target_time_min THEN 'GOOD'
        WHEN actual_time_min = target_time_min THEN 'EXPECTED'
        WHEN actual_time_min > target_time_min THEN 'WARNING'
        ELSE 'UNKNOWN'
    END AS performance_status,
    (actual_time_min - target_time_min) AS time_deviation
FROM source_data