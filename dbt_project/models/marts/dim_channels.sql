{{ config(materialized='table', schema='marts') }}

SELECT DISTINCT
    channel_name,
    ROW_NUMBER() OVER (ORDER BY channel_name) AS channel_id
FROM {{ ref('stg_telegram_messages') }}
