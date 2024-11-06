import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Router, types
from aiogram.filters import Command

from app.bot.bot import bot
from app.database.user.models import users

from app.filters.role_filters import AdminFilter

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

router = Router()


# TODO: Проверить что работа с UTC
@router.message(Command("turn_on_advertising"), AdminFilter())
async def turn_on_advertising_handler(message: types.Message):
    scheduler.start()
    # scheduler.add_job(func=advert, trigger='interval', seconds=20)
    scheduler.add_job(func=advert, trigger='date', next_run_time=datetime.datetime.utcnow() + datetime.timedelta(hours=3, seconds=120))
    await message.answer(text=f'Рассылка включена!!')
    await bot.send_message(chat_id=message.from_user.id, text="Купи премиум!!")


@router.message(Command("turn_of_advertising"), AdminFilter())
async def turn_on_advertising_handler(message: types.Message):
    scheduler.shutdown()
    await message.answer(text=f'Рассылка выключена!!')


async def advert():
    for user in users:
        await bot.send_message(chat_id=user.id, text="Купи премиум!!")
