-- Custom test: Ensure no duplicate messages per channel and date
SELECT
    channel_name,
    message_id,
    DATE(message_timestamp) AS message_date,
    COUNT(*) AS cnt
FROM {{ ref('stg_telegram_messages') }}
GROUP BY channel_name, message_id, DATE(message_timestamp)
HAVING COUNT(*) > 1
