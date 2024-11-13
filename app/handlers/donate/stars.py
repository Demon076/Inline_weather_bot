from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, PreCheckoutQuery, CallbackQuery

from app.bot.bot import bot
from app.keyboards.donate import DonateCallbackFactory

router = Router()


@router.callback_query(DonateCallbackFactory.filter(F.action == "remove"))
async def on_donate_cancel(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(DonateCallbackFactory.filter(F.action == "help"))
async def donate_help(callback: CallbackQuery):
    await callback.message.answer(
        text=f"Все средства с донатов пойдут на развитие бота. Например, на оплату сервера ))\n\n"
             f"Если вы хотите оформить рефанд, воспользуйтесь командой /refund id_транзакции\n"
             f"🤓 Вам понадобится ID транзакции."
    )


@router.message(Command("refund"))
async def refund_cmd(
        message: Message,
        command: CommandObject
):
    t_id = command.args

    if t_id is None:
        await message.answer(text="id транзакции не указан")
        return

    try:
        await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=t_id
        )
        await message.answer(text="Средства возвращены!")

    except TelegramBadRequest as e:
        err_text = "Что-то пошло не так!!"

        if "CHARGE_ALREADY_REFUNDED" in e.message:
            err_text = ("Средства уже возвращены!")

        await message.answer(err_text)
        return


@router.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery):
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(message: Message):
    await message.answer(text=f'Спасибо большое за донат!!\n\n'
                              f'Вот номер транзакции на всякий случай, если захотите вернуть средства'
                              f' {message.successful_payment.telegram_payment_charge_id}',
                         message_effect_id="5159385139981059251")
