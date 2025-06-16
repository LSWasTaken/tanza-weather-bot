import os, requests

WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
LOCATION = os.getenv('LOCATION', 'Tanza,PH')

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={WEATHER_API_KEY}&units=metric"
    r = requests.get(url)
    d = r.json()
    if r.status_code != 200:
        return f"❌ Failed: {d.get('message','Error')}"
    w, t, fl, h = d['weather'][0]['description'].capitalize(), d['main']['temp'], d['main']['feels_like'], d['main']['humidity']
    return f"🌤️ **Weather in {LOCATION}**\nCondition: {w}\nTemp: {t}°C (Feels like {fl}°C)\nHumidity: {h}%"

def send():
    d = {"content": get_weather()}
    r = requests.post(WEBHOOK_URL, json=d)
    print("✅ Sent" if r.status_code == 204 else f"❌ {r.status_code}: {r.text}")

if __name__ == "__main__":
    send()
