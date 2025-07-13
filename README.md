# Ethiopian Medical Business Data Platform

Welcome to the **Ethiopian Medical Business Data Platform**! This project builds an end-to-end data pipeline to extract, store, and transform data from public Telegram channels related to Ethiopian medical businesses (e.g., Chemed, lobelia4cosmetics, tikvahpharma). The goal is to analyze trends in medical products, pricing, visual content, and posting activity to generate actionable insights.

This README provides detailed instructions to set up the project, run the pipeline, and understand its components. Whether you're a data engineer, analyst, or new team member, this guide will help you get started quickly.

## Project Overview
The platform uses an **ELT (Extract, Load, Transform)** approach:
1. **Extract**: Scrape messages and images from Telegram channels using the `telethon` library.
2. **Load**: Store raw data as JSON files in a partitioned data lake and load them into a PostgreSQL database.
3. **Transform**: Use dbt to clean and organize data into a star schema for analytics, enabling queries like:
   - What are the top 10 most mentioned medical products?
   - How do prices vary across channels?
   - Which channels share the most images?
   - What are the daily/weekly posting trends?

## Prerequisites
Before starting, ensure you have:
- **Docker** and **Docker Compose** installed (for containerized setup).
- A **Telegram API account** (get `api_id`, `api_hash`, and `phone` from [my.telegram.org](https://my.telegram.org)).
- A text editor (e.g., VS Code) for editing configuration files.
- Basic knowledge of Python, SQL, and command-line tools.

## Project Structure
The project is organized as follows:
```
medical_data_platform/
├── data/                    # Stores raw and processed data
│   ├── raw/                 # Raw JSON files (e.g., data/raw/telegram_messages/YYYY-MM-DD/channel_name.json)
│   └── processed/           # (Future use) Processed data outputs
├── scripts/                 # Python scripts for data pipeline
│   ├── extract/             # Scraping scripts
│   │   └── telegram_scraper.py  # Scrapes Telegram messages and images
│   └── load/                # Data loading scripts
│       └── load_to_postgres.py  # Loads JSON data into PostgreSQL
├── dbt_project/             # dbt project for data transformations
│   ├── models/              # SQL models for staging and analytics
│   │   ├── staging/         # Cleans raw data (e.g., stg_telegram_messages.sql)
│   │   └── marts/           # Star schema tables (dim_channels.sql, dim_dates.sql, fct_messages.sql)
│   ├── tests/               # Data quality tests (e.g., custom_tests.sql)
│   ├── profiles.yml         # dbt database connection settings
│   ├── dbt_project.yml      # dbt project configuration
│   └── schema.yml           # Model metadata and tests
├── .env                     # Environment variables (API keys, database credentials)
├── .env.example             # Template for .env file
├── .gitignore               # Excludes sensitive files from Git
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration for Python environment
├── docker-compose.yml       # Defines app and PostgreSQL services
└── README.md                # This file
```

## Setup Instructions
Follow these steps to set up and run the project.

### 1. Clone the Repository
```bash
git clone <repository_url>
cd medical_data_platform
```

### 2. Configure Environment Variables
1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` with your credentials:
   - **Telegram API**: Add `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, and `TELEGRAM_PHONE` from [my.telegram.org](https://my.telegram.org).
   - **PostgreSQL**: Set `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST` (use `postgres` for Docker), and `POSTGRES_PORT` (default: 5432).
   Example `.env`:
   ```
   TELEGRAM_API_ID=123456
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_PHONE=+251912345678
   POSTGRES_USER=admin
   POSTGRES_PASSWORD=securepassword
   POSTGRES_DB=medical_data
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   ```
3. Ensure `.env` is not committed to Git (it’s ignored in `.gitignore`).

### 3. Build and Start Docker Containers
Run the following to start the Python app and PostgreSQL database:
```bash
docker-compose up --build -d
```
- The `-d` flag runs containers in the background.
- This builds the Python environment (from `Dockerfile`) and starts a PostgreSQL database.

### 4. Scrape Telegram Data (Task 1: Extract)
1. Run the Telegram scraping script to collect messages and images from channels (e.g., Chemed, lobelia4cosmetics, tikvahpharma):
   ```bash
   docker-compose exec app python scripts/extract/telegram_scraper.py
   ```
2. **What happens**:
   - The script uses `telethon` to connect to Telegram and scrape messages.
   - Data is saved as JSON files in `data/raw/telegram_messages/YYYY-MM-DD/channel_name.json`.
   - Images are saved in the same directory (e.g., `message_123.jpg`).
   - Logs are written to `data/scraping.log` for debugging.
3. **First-time Telegram setup**:
   - The script may prompt for a Telegram login code (sent to your phone).
   - Enter the code in the terminal to authenticate.
4. **Verify**: Check `data/raw/telegram_messages/` for JSON files and images.

### 5. Load Data into PostgreSQL (Task 1: Load)
1. Load the JSON files into the `raw.telegram_messages` table in PostgreSQL:
   ```bash
   docker-compose exec app python scripts/load/load_to_postgres.py
   ```
2. **What happens**:
   - The script creates a `raw` schema and `telegram_messages` table if they don’t exist.
   - JSON data is inserted with columns for channel, message ID, timestamp, text, image presence, and raw JSON.
   - Logs are written to `data/load.log`.
3. **Verify**: Connect to PostgreSQL and query:
   ```sql
   SELECT * FROM raw.telegram_messages LIMIT 10;
   ```
   Use a tool like `psql`:
   ```bash
   docker-compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB
   ```

### 6. Transform Data with dbt (Task 2: Transform)
1. Enter the app container to run dbt commands:
   ```bash
   docker-compose exec app bash
   ```
2. Navigate to the dbt project:
   ```bash
   cd dbt_project
   ```
3. Install dbt dependencies (e.g., `dbt_utils` for date spine):
   ```bash
   dbt deps
   ```
4. Run the dbt models to transform data:
   ```bash
   dbt run
   ```
   - **Staging Layer**: `stg_telegram_messages` cleans raw data (e.g., formats timestamps, handles nulls).
   - **Data Mart Layer**: Creates a star schema:
     - `dim_channels`: Lists unique channels with metadata (e.g., message count).
     - `dim_dates`: Provides dates for time-based analysis (2023 to July 13, 2025).
     - `fct_messages`: Links messages to channels and dates, with metrics like message length.
5. Run tests to ensure data quality:
   ```bash
   dbt test
   ```
   - Tests check for unique keys, non-null values, and no duplicate messages.
6. Generate and view documentation:
   ```bash
   dbt docs generate
   dbt docs serve --port 8080
   ```
   - Access at `http://localhost:8080` (expose port 8080 in `docker-compose.yml` if needed).
7. **Verify**: Query the transformed tables:
   ```sql
   SELECT * FROM marts.fct_messages LIMIT 10;
   SELECT channel_name, COUNT(*) FROM marts.fct_messages JOIN marts.dim_channels ON fct_messages.channel_id = dim_channels.channel_id GROUP BY channel_name;
   ```

## Analyzing Data
The transformed data in `marts.fct_messages`, `marts.dim_channels`, and `marts.dim_dates` supports queries like:
- **Top 10 products**: `SELECT message_text, COUNT(*) FROM marts.fct_messages GROUP BY message_text ORDER BY COUNT(*) DESC LIMIT 10;`
- **Daily trends**: `SELECT d.date, COUNT(*) FROM marts.fct_messages f JOIN marts.dim_dates d ON f.date_id = d.date_id GROUP BY d.date;`
- **Image-heavy channels**: `SELECT c.channel_name, SUM(CASE WHEN f.has_image THEN 1 ELSE 0 END) FROM marts.fct_messages f JOIN marts.dim_channels c ON f.channel_id = c.channel_id GROUP BY c.channel_name;`

## Troubleshooting
- **Docker issues**: Ensure Docker is running and ports (5432, 8080) are free. Check logs: `docker-compose logs`.
- **Telegram API errors**: Verify `api_id`, `api_hash`, and `phone` in `.env`. If rate-limited, wait and retry.
- **dbt errors**: Ensure PostgreSQL is running and `raw.telegram_messages` has data. Check `dbt_project/logs/dbt.log`.
- **No data in tables**: Confirm scraping and loading steps completed successfully