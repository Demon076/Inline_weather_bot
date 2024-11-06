from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from app.database.user.models import User


class MenuCallbackFactory(CallbackData, prefix="fab_menu"):
    action: str


def base_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="Открыть инлайн режим бота",
                switch_inline_query_current_chat=""
            )
        ]])


def menu_keyboard(user: User) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Открыть инлайн режим бота",
        switch_inline_query_current_chat=""
    )
    builder.button(
        text="Показать погоду по местоположению",
        callback_data=MenuCallbackFactory(action="location_weather")
    )
    builder.button(
            text="Местоположение",
            callback_data=MenuCallbackFactory(action="location")
    )
    builder.button(
        text="Настроить рассылку погоды",
        callback_data=MenuCallbackFactory(action="sending_weather")
    )

    builder.adjust(1)
    return builder.as_markup()
