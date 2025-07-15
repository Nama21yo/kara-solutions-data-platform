from dagster import job
from ops.scrape import scrape_telegram_data
from ops.load_raw import load_raw_to_postgres
from ops.run_dbt import run_dbt_transformations
from ops.yolo_enrich import run_yolo_enrichment

@job
def kara_data_pipeline():
    raw = scrape_telegram_data()
    loaded = load_raw_to_postgres(raw)
    transformed = run_dbt_transformations(loaded)
    run_yolo_enrichment(transformed)
