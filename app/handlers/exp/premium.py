from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()
router.message.filter(F.chat.type == "private")


@router.message(Command("donate", "donat", "донат"))
async def cmd_donate(message: Message, command: CommandObject):
    if command.args is None or not command.args.isdigit() or not 1 <= int(command.args) <= 2500:
        await message.answer("Вы не ввели количество звёзд для доната")
        return

    amount = int(command.args)

    kb = InlineKeyboardBuilder()
    kb.button(
        text=f'Заплатить {amount} звёзд',
        pay=True
    )
    kb.button(
        text=f'Отказаться от доната ((',
        callback_data="donate_cancel"
    )
    kb.adjust(1)

    prices = [LabeledPrice(label="XTR", amount=amount)]

    await message.answer_invoice(
        title=f'Ура!!!',
        description=f'Если задонатите столько буду благодарен!!!',
        prices=prices,

        provider_token="",

        payload=f"{amount}_stars",

        currency="XTR",

        reply_markup=kb.as_markup()
    )


@router.callback_query(F.data == "donate_cancel")
async def on_donate_cancel(callback: CallbackQuery):
    await callback.answer(text="А жаль")

    await callback.message.delete()


@router.message(Command("paysupport"))
async def cmd_paysupport(message: Message):
    await message.answer(text=f"Если вы хотите оформить рефанд, воспользуйтесь командой /refund"
                              f"🤓 Вам понадобится ID транзакции.")


@router.message(Command("refund"))
async def cmd_refund(message: Message, bot: Bot, command: CommandObject):
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
    # смысл on_pre_checkout_query такой же, как и в любых других платежах
    # бот должен ответить в течение 10 секунд
    # ..
    # тут можно/нужно проверить доступность товара/услуги, прямо перед оплатой
    # ..
    # так как у нас просто донат, мы просто всегда отвечаем положительно
    await query.answer(ok=True)

    # либо вот так, если по какой-то причине надо отказать в проведении платежа
    # await query.answer(
    #    ok=False,
    #    error_message="Причина почему отказывем (прим. кончился товар)"
    # )


@router.message(F.successful_payment)
async def on_successfull_payment(message: Message):
    # И наконец обработка УСПЕШНОГО ПЛАТЕЖА
    # тут мы получаем объект message.successful_payment
    # в котором содержится ID транзакции, пэйлод который мы указывали при создании инвойса
    # и все такое прочее
    # ..
    # мы же просто передаем сообщение об успешном донате

    await message.answer(text=f'Оплата успешно {message.successful_payment.telegram_payment_charge_id}!!',

        # добавляем к сообщению эффект "сердечка" из стандартных реакций
        message_effect_id="5159385139981059251",

        # другие реакции (если надо)
        # 🔥 огонь - 5104841245755180586
        # 👍 лайк - 5107584321108051014
        # 👎 дизлайк - 5104858069142078462
        # ❤️ сердечко - 5159385139981059251
        # 🎉 праздник - 5046509860389126442
        # 💩 какаха - 5046589136895476101
    )
