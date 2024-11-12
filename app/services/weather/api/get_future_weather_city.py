import logging

from app.services.weather import api_openweathermap, api_wttr
from app.services.weather.FutureWeather import FutureWeather
from app.services.weather.city import City


async def get_future_weather_city(city: City) -> FutureWeather:
    try:
        weather = await api_openweathermap.get_weather_future.get_weather_future(
            lat=city.lat,
            lon=city.lon
        )
        return weather
    except Exception as ex:
        logging.error(f"Не сработал первый способ в current_future_weather_city! {ex}")

    try:
        weather = await api_wttr.get_weather.get_weather_days(
            city=city.name_en
        )
        return weather
    except Exception as ex:
        logging.error(f"Не сработал второй способ в current_future_weather_city! {ex}")
