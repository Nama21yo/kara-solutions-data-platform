from dagster import op

@op
def scrape_telegram_data(context):
    context.log.info("Scraping telegram data...")
    # call your existing scrape script
    return "raw_data_path"
