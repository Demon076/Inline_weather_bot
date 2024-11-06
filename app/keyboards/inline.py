from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class WeatherCallbackFactory(CallbackData, prefix="fab_weather"):
    action: str
    city_id: int


class PaginatorCallbackFactory(CallbackData, prefix="fab_paginator"):
    index_paginator: int


def city_keyboard(city: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Показать погоду сейчас",
        callback_data=WeatherCallbackFactory(action="current", city_id=city)
    )
    builder.button(
        text="Показать погоду почасовую",
        callback_data=WeatherCallbackFactory(action="future_hour", city_id=city)
    )
    builder.button(
        text="Показать погоду по дням",
        callback_data=WeatherCallbackFactory(action="future_day", city_id=city)
    )
    builder.adjust(1)
    return builder.as_markup()
