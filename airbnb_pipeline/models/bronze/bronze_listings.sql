{{ config(materialized='incremental')}}
{% set incremental_column = 'CREATED_AT' %}

SELECT 
    *
FROM    
    {{ source('staging','listings')}}
{% if is_incremental() %}
    WHERE
        {{ incremental_column }} > (SELECT COALESCE(MAX({{incremental_column}}),'1970-01-01') FROM {{ this }})
{% endif %}