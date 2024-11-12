import logging

from app.services.weather import api_weatherapi, api_openweathermap, api_wttr
from app.services.weather.Weather import Weather
from app.services.weather.city import City


async def get_weather_city(city: City) -> Weather:
    try:
        weather = await api_openweathermap.get_weather.get_weather_coordinates(
            lat=city.lat,
            lon=city.lon
        )
        return weather
    except Exception as ex:
        logging.error(f"Не сработал первый способ в current_weather_city! {ex}")

    try:
        weather = await api_wttr.get_weather.get_weather_current(
            city=city.name_en
        )
        return weather
    except Exception as ex:
        logging.error(f"Не сработал второй способ в current_weather_city! {ex}")

    try:
        weather = await api_weatherapi.get_weather_coordinates(
            latitude=city.lat,
            longitude=city.lon
        )
        return weather
    except Exception as ex:
        logging.error(f"Не сработал третий способ в current_weather! {ex}")
