# app/services/weather.py
import httpx
from app.config import settings

async def get_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.weather_api_key}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "description": data["weather"][0]["description"].capitalize(),
                "temperature": round(data["main"]["temp"], 1),
                "city": data["name"]
            }
        return {"error": "Invalid city name or network error."}
