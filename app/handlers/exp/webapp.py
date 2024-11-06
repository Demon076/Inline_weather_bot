from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import WebAppInfo

router = Router()


@router.message(Command("horo"))
async def location_handler(message: types.Message):
    kb = [[
        InlineKeyboardButton(
            text=f'Открыть гороскоп',
            web_app=WebAppInfo(url="https://horo.mail.ru/prediction/scorpio/today/")
        )
    ]]
    await message.answer(text=f'Можно посмотреть гороскоп прямо в телеграмме',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
                         )
