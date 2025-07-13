{{ config(
    materialized='view',
    schema='staging',
    alias='telegram_messages'
) }}

SELECT
    id AS raw_id,
    channel AS channel_name,
    message_id,
    CAST(message_date AS TIMESTAMP) AS message_timestamp,
    COALESCE(message_text, '') AS message_text,
    has_image,
    image_path,
    raw_data
FROM {{ source('raw', 'telegram_messages') }}
WHERE message_id IS NOT NULL
  AND message_date IS NOT NULL
