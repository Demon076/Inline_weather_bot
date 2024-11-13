import emoji

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class DonateCallbackFactory(CallbackData, prefix="fab_donate"):
    action: str


def donate_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=f'Отправить 1 звёздочку',
        pay=True
    )
    kb.button(
        text=f'Задонатить через крипту {emoji.emojize("💰")}',
        url=f'https://cwallet.com/t/HIYA6RJ1'
    )
    kb.button(
        text="Узнать больше о донате",
        callback_data=DonateCallbackFactory(action="help")
    )
    kb.button(
        text=f'Отказаться от доната ((',
        callback_data=DonateCallbackFactory(action="remove")
    )
    kb.adjust(1)

    return kb.as_markup()
