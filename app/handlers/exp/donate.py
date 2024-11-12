import emoji
from typing import List
from aiogram.types import CallbackQuery
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


router = Router()


@router.message(Command("donate_c"))
async def location_handler(message: types.Message):
    kb = [[
        InlineKeyboardButton(
            text=f'Задонатить через CWallet {emoji.emojize("💰")}',
            url=f'https://cwallet.com/t/HIYA6RJ1'
        )
    ]]
    await message.answer(text=f'При желании можно задонатить нажав на кнопки ниже ^_^',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
                         )
