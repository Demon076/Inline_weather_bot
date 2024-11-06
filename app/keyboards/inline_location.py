from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards.inline import WeatherCallbackFactory


def inline_location_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Показать погоду сейчас",
        callback_data=WeatherCallbackFactory(action="location_current", city_id=-1)
    )
    builder.adjust(1)
    return builder.as_markup()
