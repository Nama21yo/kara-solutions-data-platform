{{ config(materialized='view', schema='staging') }}

SELECT
    id,
    channel AS channel_name,
    message_id,
    message_date::TIMESTAMP AS message_date,
    COALESCE(message_text, '') AS message_text,
    has_image,
    image_path,
    raw_data
FROM raw.telegram_messages
WHERE message_date IS NOT NULL
