from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class CapchaCallbackFactory(CallbackData, prefix="fab_capcha"):
    answer: int
    right: bool


def capcha_keyboard(answers: List[int], right_answer: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for answer in answers:
        right = False
        if answer == right_answer:
            right = True
        builder.button(
            text=f'{answer}',
            callback_data=CapchaCallbackFactory(answer=answer, right=right)
        )

    return builder.as_markup()
