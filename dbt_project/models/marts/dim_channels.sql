{{ config(
    materialized='table',
    schema='marts',
    unique_key='channel_id'
) }}

SELECT
    ROW_NUMBER() OVER () AS channel_id,
    channel_name,
    COUNT(*) AS total_messages,
    MIN(message_timestamp) AS first_message_timestamp,
    MAX(message_timestamp) AS last_message_timestamp
FROM {{ ref('stg_telegram_messages') }}
GROUP BY channel_name
