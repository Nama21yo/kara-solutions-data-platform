# Medical Data Platform

This project builds an ELT pipeline to analyze data from Ethiopian medical business Telegram channels.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd medical_data_platform
   ```

2. Create a `.env` file based on `.env.example` and fill in your Telegram API and PostgreSQL credentials.

3. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

4. Run the scraping script:
   ```bash
   docker-compose exec app python scripts/extract/telegram_scraper.py
   ```

## Project Structure
- `data/`: Stores raw and processed data.
- `scripts/`: Contains Python scripts for extraction and loading.
- `dbt_project/`: DBT models for transformation.

## Requirements
- Docker
- Docker Compose
- Python 3.11