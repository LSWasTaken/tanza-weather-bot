import requests
import os

city = "Tanza,PH"
api_key = os.getenv("OWM_API_KEY")
bgh_key = os.getenv("BGH_API_KEY")
webhook_url = os.getenv("WEBHOOK_URL")

if not all([api_key, bgh_key, webhook_url]):
    raise ValueError("Missing environment variable(s): Check OWM_API_KEY, BGH_API_KEY, and WEBHOOK_URL.")

weather_api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(weather_api)
weather_data = response.json()

if "main" not in weather_data or "weather" not in weather_data:
    error_message = weather_data.get("message", "Unexpected API response")
    print("Failed to fetch weather:", error_message)
    exit(1)

temp = weather_data["main"]["temp"]
desc = weather_data["weather"][0]["description"].title()
humidity = weather_data["main"]["humidity"]

weather_icons = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Thunderstorm": "⛈️",
    "Drizzle": "🌦️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌁",
    "Haze": "🌤️"
}
condition_main = weather_data["weather"][0]["main"]
icon = weather_icons.get(condition_main, "🌍")

message = f"""```diff
- Weather in {city}
+ Condition: {desc} {icon}
+ Temperature: {temp}°C
+ Humidity: {humidity}%
```"""

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

post_response = requests.post(webhook_url, json=payload, headers=headers)
print("Webhook sent:", post_response.status_code)
print("Response text:", post_response.text)
