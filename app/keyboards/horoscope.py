from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.user.enums import ZodiacSign
from app.database.user.models import User
from app.keyboards.base import MenuCallbackFactory
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class HoroscopeCallbackFactory(CallbackData, prefix="fab_horo"):
    zodiac_sign: str


def horoscope_keyboard(user: User) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for sign in ZodiacSign.list_zodiac_signs():
        builder.button(
            text=sign.russian_name(),
            callback_data=HoroscopeCallbackFactory(
                zodiac_sign=sign.value
            )
        )
    builder.adjust(2)

    if user.horoscope is not None:
        builder.row(InlineKeyboardButton(
            text="Удалить знак зодиака",
            callback_data=HoroscopeCallbackFactory(zodiac_sign="delete").pack()
        ))

    builder.row(InlineKeyboardButton(
        text="Вернуться",
        callback_data=MenuCallbackFactory(action="sending_weather").pack()
    ))
    return builder.as_markup()
