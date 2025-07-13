{{ config(
    materialized='table',
    schema='marts',
    unique_key='message_key'
) }}

SELECT
    CONCAT(s.message_id, '_', s.channel_name) AS message_key,
    c.channel_id,
    d.date_id,
    s.message_timestamp,
    s.message_text,
    LENGTH(COALESCE(s.message_text, '')) AS message_length,
    s.has_image,
    s.image_path
FROM {{ ref('stg_telegram_messages') }} s
JOIN {{ ref('dim_channels') }} c ON s.channel_name = c.channel_name
JOIN {{ ref('dim_dates') }} d ON DATE(s.message_timestamp) = d.date
