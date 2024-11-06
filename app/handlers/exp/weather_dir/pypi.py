from datetime import datetime, time
from typing import List

import python_weather
from python_weather.forecast import DailyForecast

import asyncio

from app.services.weather.FutureWeather import FutureWeather
from app.services.weather.Weather import Weather


async def get_weather_current(city: str) -> Weather:
    async with python_weather.Client(unit=python_weather.METRIC, locale=python_weather.Locale.RUSSIAN) as client:
        weather = await client.get(city)
        weather = Weather(
            temp=round(weather.temperature, 1),
            temp_feels_like=round(weather.feels_like, 1),
            weather_main=weather.description,
            wind_speed=round((weather.wind_speed * 1000) / 3600, 2),
            date=weather.datetime
        )

        return weather


async def get_weather_days(city: str) -> FutureWeather:
    async with python_weather.Client(unit=python_weather.METRIC,
                                     locale=python_weather.Locale.RUSSIAN) as client:
        weather = await client.get(city)

        future_weather = []

        for daily in weather:
            daily_date: datetime.date = daily.date
            index = -1
            for hourly in daily:
                index += 1
                daily_date = datetime.combine(daily_date, time(3 * index, 0))

                future_weather.append(Weather(
                    temp=round(hourly.temperature, 1),
                    temp_feels_like=round(hourly.feels_like, 1),
                    weather_main=hourly.description,
                    wind_speed=round((hourly.wind_speed * 1000) / 3600, 2),
                    date=daily_date
                ))

        return FutureWeather(future_weather)


async def main():
    weather = await get_weather_current('Yaroslavl')
    future_weather = await get_weather_days('Yaroslavl')

    print(weather.rus_string())
    print(future_weather.future_day())
    print(future_weather.future_hour(3))


if __name__ == '__main__':
    asyncio.run(main())
