import requests
import os

city = "Tanza,PH"
api_key = os.getenv("OWM_API_KEY")
bgh_key = os.getenv("BGH_API_KEY")
webhook_url = os.getenv("WEBHOOK_URL")

# Get weather data
weather_api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
weather_data = requests.get(weather_api).json()

temp = weather_data["main"]["temp"]
desc = weather_data["weather"][0]["description"].title()
humidity = weather_data["main"]["humidity"]

message = f"{desc}, {temp}°C, Humidity: {humidity}%"

# Send to BotGhost webhook
payload = {
    "variables": [
        {
            "name": "weather",
            "variable": "{weather}",
            "value": message
        }
    ]
}
headers = {
    "Authorization": bgh_key,
    "Content-Type": "application/json"
}
response = requests.post(webhook_url, json=payload, headers=headers)
print("Webhook sent:", response.status_code)
