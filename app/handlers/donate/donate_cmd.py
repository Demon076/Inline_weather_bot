from aiogram import Router, types
from aiogram.filters import Command
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery
from app.keyboards.donate import donate_keyboard

router = Router()


@router.message(Command("donate"))
async def donate_cmd(message: types.Message):
    prices = [LabeledPrice(label="XTR", amount=1)]
    await message.answer_invoice(
        title=f'Донатик ^_^',
        description=f'При желании можно задонатить нажав на кнопки ниже:',
        prices=prices,

        provider_token="",

        payload=f"1_stars",

        currency="XTR",

        reply_markup=donate_keyboard()
    )
