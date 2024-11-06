from aiohttp import ClientSession

from app.bot.settings import bot_settings
from app.services.weather.Weather import Weather
from app.services.weather.api import RateLimiter


async def get_weather(city: str) -> Weather:
    await RateLimiter.request_api()
    client_session = ClientSession()
    async with client_session as session:
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': bot_settings.WEATHER}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            weather = Weather.json_to_weather(weather_json)
            return weather


async def get_weather_coordinates(lat: float, lon: float) -> Weather:
    await RateLimiter.request_api()
    client_session = ClientSession()
    async with client_session as session:
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'lat': lat, 'lon': lon, 'APPID': bot_settings.WEATHER}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            weather = Weather.json_to_weather(weather_json)
            return weather
