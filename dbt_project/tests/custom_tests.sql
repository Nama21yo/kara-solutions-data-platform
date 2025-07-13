-- Custom test: No duplicate messages per channel and date
SELECT
    channel_name,
    message_id,
    DATE(message_timestamp) AS message_date,
    COUNT(*) AS cnt
FROM {{ ref('stg_telegram_messages') }}
GROUP BY channel_name, message_id, DATE(message_timestamp)
HAVING COUNT(*) > 1

-- Custom test: has_image consistency with image_path
SELECT
    message_key,
    has_image,
    image_path
FROM {{ ref('fct_messages') }}
WHERE has_image = TRUE AND (image_path IS NULL OR image_path = '')
