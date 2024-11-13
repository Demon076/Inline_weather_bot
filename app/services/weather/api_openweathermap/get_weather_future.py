from aiohttp import ClientSession

from app.bot.settings import bot_settings
from app.services.weather.FutureWeather import FutureWeather
from app.services.weather.api_openweathermap.rate_limiter import RateLimiter


# TODO: Добавить кэширование запросов 
async def get_weather_future(lat: float, lon: float) -> FutureWeather:
    await RateLimiter.request_api()
    client_session = ClientSession()
    async with client_session as session:
        url = 'https://api.openweathermap.org/data/2.5/forecast'
        params = {'lat': lat, 'lon': lon, 'APPID': bot_settings.WEATHER}

        async with session.get(url=url, params=params) as response:
            json_future_weather = await response.json()
            future_weather = FutureWeather.json_to_future_weather_list(json_future_weather)
            return future_weather
