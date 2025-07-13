{{ config(
    materialized='table',
    schema='marts',
    unique_key='date_id'
) }}

WITH date_spine AS (
  {{ dbt_utils.date_spine(
      datepart="day",
      start_date="CAST('{{ var('start_date') }}' AS DATE)",
      end_date="CAST('{{ var('end_date') }}' AS DATE)"
  ) }}
)
SELECT
    ROW_NUMBER() OVER () AS date_id,
    date_day AS date,
    EXTRACT(YEAR FROM date_day) AS year,
    EXTRACT(MONTH FROM date_day) AS month,
    EXTRACT(DAY FROM date_day) AS day,
    EXTRACT(DOW FROM date_day) AS day_of_week,
    EXTRACT(WEEK FROM date_day) AS week_of_year
FROM date_spine
