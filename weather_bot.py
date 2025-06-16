import os
import requests
from datetime import datetime

WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
LOCATION = os.getenv('LOCATION', 'Tanza,PH')

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return f"❌ Failed to fetch weather: {data.get('message', 'Unknown error')}"

    weather = data['weather'][0]['description'].capitalize()
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %I:%M %p (UTC)')

    message = (
        f"🌤️ **Weather Update: Tanza, Cavite**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"**🌡 Temperature:** {temp}°C (Feels like {feels_like}°C)\n"
        f"**🌬️ Condition:** {weather}\n"
        f"**💧 Humidity:** {humidity}%\n"
        f"**🕒 Last Updated:** {timestamp}"
    )
    return message

def send_to_discord(message):
    data = {
        "content": message
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("✅ Weather sent to Discord.")
    else:
        print(f"❌ Failed to send: {response.status_code} - {response.text}")

if __name__ == "__main__":
    message = get_weather()
    send_to_discord(message)
