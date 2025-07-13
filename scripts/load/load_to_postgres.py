import os
import json
from pathlib import Path
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    filename='data/load.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# PostgreSQL connection
conn_params = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT')
}

def create_raw_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS raw;
            CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                id SERIAL PRIMARY KEY,
                channel VARCHAR(255),
                message_id INTEGER,
                message_date TIMESTAMP,
                message_text TEXT,
                has_image BOOLEAN,
                image_path TEXT,
                raw_data JSONB
            );
        """)
        conn.commit()
        logging.info("Created raw.telegram_messages table")

def load_json_to_postgres(json_file, channel, conn):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            messages = json.load(f)
        
        with conn.cursor() as cur:
            for msg in messages:
                cur.execute("""
                    INSERT INTO raw.telegram_messages (
                        channel, message_id, message_date, message_text, 
                        has_image, image_path, raw_data
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    channel,
                    msg['id'],
                    msg['date'],
                    msg['text'],
                    msg['has_image'],
                    msg.get('image_path'),
                    Json(msg)
                ))
            conn.commit()
            logging.info(f"Loaded {len(messages)} messages from {json_file}")
    except Exception as e:
        logging.error(f"Error loading {json_file}: {str(e)}")
        conn.rollback()

def main():
    data_dir = Path('data/raw/telegram_messages')
    conn = psycopg2.connect(**conn_params)
    
    create_raw_table(conn)
    
    for date_dir in data_dir.iterdir():
        if date_dir.is_dir():
            for channel_dir in date_dir.iterdir():
                if channel_dir.is_dir():
                    json_file = channel_dir / 'messages.json'
                    if json_file.exists():
                        load_json_to_postgres(json_file, channel_dir.name, conn)
    
    conn.close()

if __name__ == '__main__':
    main()
