import random
from typing import List
from aiogram.types import CallbackQuery
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from app.database.user.models import User
from app.keyboards.capcha import CapchaCallbackFactory, capcha_keyboard

router = Router()


@router.message(Command("capcha"))
async def capcha_cmd(message: types.Message):
    num1 = random.randint(0, 15)
    num2 = random.randint(0, 15)
    right_answer = num1 + num2
    position_right_answer = random.randint(0, 3)
    answers = []

    for i in range(4):
        answers.append(random.randint(0, 30))
        if answers[i] == right_answer:
            answers[i] += 1
    answers[position_right_answer] = right_answer

    await message.answer(
        text=f'Чтобы начать пользоваться ботом ответьте на задачку {num1}+{num2}=',
        reply_markup=capcha_keyboard(answers, right_answer)
    )


@router.callback_query(CapchaCallbackFactory.filter())
async def current_weather_call(
        callback: CallbackQuery,
        callback_data: CapchaCallbackFactory
):
    if callback_data.right:
        User.get_by_id_or_create(callback.from_user)
        await callback.message.answer(text="Ура всё получилось!!")
    else:
        await callback.message.answer(text="Ответ неверный!!")
        await capcha_cmd(callback.message)

    await callback.message.delete()
