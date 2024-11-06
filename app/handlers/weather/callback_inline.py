from typing import List

import emoji
from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.bot.bot import bot
from app.keyboards.inline import WeatherCallbackFactory
from app.services.weather.Weather import Weather
from app.services.weather.api.get_weather import get_weather_coordinates
from app.services.weather.api.get_weather_future import get_weather_future
from app.services.weather.data import Cities

router = Router()


@router.callback_query(WeatherCallbackFactory.filter(F.action == "current"))
async def current_weather_call(
        callback: CallbackQuery,
        callback_data: WeatherCallbackFactory
):
    city = Cities.dict_cities_id[callback_data.city_id]
    weather = await get_weather_coordinates(lat=city.lat, lon=city.lon)
    await bot.edit_message_text(
        inline_message_id=callback.inline_message_id,
        text=f'*{city.name_ru}*\n\n'
             f'{weather.rus_string()}',
        parse_mode="Markdown"
    )


@router.callback_query(WeatherCallbackFactory.filter(F.action == "future_hour"))
async def future_weather_hour_call(
        callback: CallbackQuery,
        callback_data: WeatherCallbackFactory
):
    city = Cities.dict_cities_id[callback_data.city_id]
    future_weather = await get_weather_future(lat=city.lat, lon=city.lon)
    await bot.edit_message_text(
        inline_message_id=callback.inline_message_id,
        text=f'*{city.name_ru}*\n\n'
             f'{future_weather_to_string(future_weather.future_hour(time_zone=city.time_zone))}',
        parse_mode="Markdown"
    )


@router.callback_query(WeatherCallbackFactory.filter(F.action == "future_day"))
async def future_weather_day_call(
        callback: CallbackQuery,
        callback_data: WeatherCallbackFactory
):
    city = Cities.dict_cities_id[callback_data.city_id]
    future_weather = await get_weather_future(lat=city.lat, lon=city.lon)
    await bot.edit_message_text(
        inline_message_id=callback.inline_message_id,
        text=f'*{city.name_ru}*\n\n'
             f'{future_weather_to_string(future_weather.future_day())}',
        parse_mode="Markdown"
    )


def future_weather_to_string(future_weather: List[Weather]) -> str:
    answer = ""
    flag = future_weather[0].date.hour != future_weather[1].date.hour
    emoji_clock = emoji.emojize("⏰")
    emoji_calendar = emoji.emojize("🗓️")
    for index, weather in enumerate(future_weather):
        if flag:
            answer += f'{emoji_clock} {weather.date.strftime("%H:%M")}\n'
        answer += f'{emoji_calendar} {weather.date.strftime("%d.%m.%Y")}\n'
        answer += weather.rus_string()
        answer += "\n\n"
    return answer
