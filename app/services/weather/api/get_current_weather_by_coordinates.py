import logging

from app.services.weather import api_weatherapi, api_openweathermap
from app.services.weather.Weather import Weather


async def get_weather_by_coordinates(latitude: float, longitude: float) -> Weather:
    try:
        weather = await api_weatherapi.get_weather_coordinates(latitude, longitude)
        return weather
    except Exception as ex:
        logging.error(f"Не сработал первый способ в current_weather! {ex}")

    try:
        weather = await api_openweathermap.get_weather.get_weather_coordinates(
            lat=latitude,
            lon=longitude
        )
        return weather
    except Exception as ex:
        logging.error(f"Не сработал второй способ в current_weather! {ex}")
