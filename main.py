from pyrogram import Client
from pyrogram.types import InputMediaPhoto
import requests
import schedule
import time
import threading

# Your API ID and API hash
API_ID = "29301453"
API_HASH = "aaf265964f64b744218fbebdd79c5319"
# Your bot token
API_TOKEN = "7184440378:AAEV7Yk0ByDEyufRpWJ1AUgrczne0byFjuM"
# Your channel username or ID
CHANNEL_ID = "@awehr4rea4herh"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=API_TOKEN)

# Function to fetch and send news updates
def send_news_updates():
    news_api_url = "https://api.coingecko.com/api/v3/news"
    response = requests.get(news_api_url)
    if response.status_code == 200:
        try:
            data = response.json().get("data", [])
            for article in data:
                title = article.get('title', 'No Title')
                description = article.get('description', 'No description')
                url = article.get('url', 'No URL')
                image_url = article.get('thumb_2x')
                # Send news update to channel
                if image_url:
                    app.send_media_group(
                        chat_id=CHANNEL_ID,
                        media=[
                            InputMediaPhoto(media=image_url, caption=f"<b>{title}</b>\n{description}\n\n<a href='{url}'>Read more...</a>")
                        ]
                    )
                else:
                    app.send_message(
                        chat_id=CHANNEL_ID,
                        text=f"<b>{title}</b>\n<a href='{url}'>Read more...</a>",
                        parse_mode="html"
                    )
        except Exception as e:
            print("Error parsing response:", e)

# Function to start the scheduler
def start_scheduler():
    # Schedule news fetching every hour
    schedule.every().second.do(send_news_updates)

    # Run the scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=start_scheduler)
scheduler_thread.start()

# Run the Pyrogram client's event loop
app.run()
