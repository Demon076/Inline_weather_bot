import enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ActionCallbackAdmin(enum.Enum):
    edit_ru_name = "edit_ru_name"


class WeatherCallbackFactory(CallbackData, prefix="fab_admin"):
    action: ActionCallbackAdmin
    city_id: int


def admin_add_city_keyboard(city: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Поменять русское название",
        callback_data=WeatherCallbackFactory(action=ActionCallbackAdmin.edit_ru_name, city_id=city)
    )
    return builder.as_markup()
