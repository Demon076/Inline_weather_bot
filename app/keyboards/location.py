from app.database.user.models import User
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from app.keyboards.base import MenuCallbackFactory


class LocationCallbackFactory(CallbackData, prefix="fab_location"):
    action: str


def location_keyboard(user: User, return_callback_data: CallbackData | str = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if user.location is None:
        builder.button(
            text="Запомнить местоположение",
            callback_data=LocationCallbackFactory(action="remember_location")
        )
    else:
        builder.button(
            text="Запомнить другое местоположение",
            callback_data=LocationCallbackFactory(action="remember_location")
        )
        builder.button(
            text="Удалить местоположение",
            callback_data=LocationCallbackFactory(action="forget_location")
        )
    if return_callback_data is not None:
        builder.button(
            text="Вернуться",
            callback_data=return_callback_data
        )
    builder.adjust(1)
    return builder.as_markup()
