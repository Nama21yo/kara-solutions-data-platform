from dagster import schedule
from repo import kara_data_pipeline

@schedule(cron_schedule="0 0 * * *", job=kara_data_pipeline)
def daily_pipeline_schedule(_context):
    return {}
