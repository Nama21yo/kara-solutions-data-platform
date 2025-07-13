import os
import json
import logging
from datetime import datetime
from pathlib import Path
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    filename='data/scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Telegram API credentials
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')

# Channels to scrape
channels = [
    'chemed123',
    'lobelia4cosmetics',
    'tikvahpharma'
]

async def scrape_channel(client, channel):
    data_dir = Path(f"data/raw/telegram_messages/{datetime.now().strftime('%Y-%m-%d')}/{channel}")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    messages = []
    try:
        async for message in client.iter_messages(channel, limit=100):
            message_data = {
                'id': message.id,
                'date': message.date.isoformat(),
                'text': message.text,
                'has_image': isinstance(message.media, MessageMediaPhoto)
            }
            if message_data['has_image']:
                image_path = data_dir / f"message_{message.id}.jpg"
                await message.download_media(file=image_path)
                message_data['image_path'] = str(image_path)
            messages.append(message_data)
        
        # Save to JSON
        output_file = data_dir / 'messages.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        logging.info(f"Scraped {len(messages)} messages from {channel}")
    except Exception as e:
        logging.error(f"Error scraping {channel}: {str(e)}")

async def main():
    async with TelegramClient('session', api_id, api_hash) as client:
        await client.start(phone=phone)
        for channel in channels:
            await scrape_channel(client, channel)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
