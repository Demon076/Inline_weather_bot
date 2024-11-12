import emoji

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

def donate_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text=f'Задонатить через CWallet {emoji.emojize("💰")}',
            url=f'https://cwallet.com/t/HIYA6RJ1'
        )
    ]])


@router.message(Command("donate"))
async def donate_cmd(message: types.Message):
    await message.answer(text=f'При желании можно задонатить нажав на кнопки ниже ^_^',
                         reply_markup=donate_keyboard()
                         )
