import requests
import schedule
import asyncio
import discord
from datetime import datetime, timedelta
import time

BOT_TOKEN = "your_discord_bot_token"
CHANNEL_ID = your_channel_id  # Replace with your Discord channel ID

def get_sun_times(lat, lon):
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&formatted=0"
    response = requests.get(url)
    data = response.json()['results']
    return data['sunrise'], data['sunset']

async def send_discord_message(message):
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        channel = client.get_channel(CHANNEL_ID)
        await channel.send(message)
        await client.close()

    await client.start(BOT_TOKEN)

def schedule_notifications(sunrise, sunset):
    sunrise_time = datetime.fromisoformat(sunrise).astimezone()
    sunset_time = datetime.fromisoformat(sunset).astimezone()

    schedule.every().day.at((sunrise_time - timedelta(minutes=35)).strftime('%H:%M')).do(
        asyncio.run, send_discord_message("35 minutes until sunrise!")
    )
    schedule.every().day.at(sunrise_time.strftime('%H:%M')).do(
        asyncio.run, send_discord_message("Sunrise is happening now!")
    )
    schedule.every().day.at((sunrise_time + timedelta(minutes=35)).strftime('%H:%M')).do(
        asyncio.run, send_discord_message("35 minutes after sunrise!")
    )
    schedule.every().day.at((sunset_time - timedelta(minutes=35)).strftime('%H:%M')).do(
        asyncio.run, send_discord_message("35 minutes until sunset!")
    )
    schedule.every().day.at(sunset_time.strftime('%H:%M')).do(
        asyncio.run, send_discord_message("Sunset is happening now!")
    )

if __name__ == "__main__":
    lat, lon = 34.0522, -118.2437  # Example coordinates for Los Angeles
    sunrise, sunset = get_sun_times(lat, lon)
    schedule_notifications(sunrise, sunset)

    while True:
        schedule.run_pending()
        time.sleep(1)
