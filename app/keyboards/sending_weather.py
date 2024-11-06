from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.user.enums import ZodiacSign
from app.database.user.models import User
from app.keyboards.base import MenuCallbackFactory
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# TODO: Возможно лучше заменять на CF CallbackFactory
class SendingWeatherMenuCallbackFactory(CallbackData, prefix="fab_swmenu"):
    action: str


def return_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Вернуться",
        callback_data=MenuCallbackFactory(action="sending_weather")
    )
    builder.adjust(1)
    return builder.as_markup()


def menu_keyboard(user: User) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if user.sending_weather:
        builder.button(
            text="Выключить",
            callback_data=SendingWeatherMenuCallbackFactory(action="turn_off")
        )
    else:
        builder.button(
            text="Включить",
            callback_data=SendingWeatherMenuCallbackFactory(action="turn_on")
        )

    builder.button(
        text="Местоположение",
        callback_data=SendingWeatherMenuCallbackFactory(action="location")
    )
    if user.time_is_set():
        builder.button(
            text="Удалить время",
            callback_data=SendingWeatherMenuCallbackFactory(action="forget_time")
        )
    else:
        builder.button(
            text="Задать время",
            callback_data=SendingWeatherMenuCallbackFactory(action="time")
        )

    builder.button(
        text="Гороскоп",
        callback_data=SendingWeatherMenuCallbackFactory(action="horoscope")
    )
    builder.button(
        text="Вернуться",
        callback_data="menu"
    )
    builder.adjust(1)
    return builder.as_markup()

