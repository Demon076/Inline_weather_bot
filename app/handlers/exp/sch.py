import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Router, types
from aiogram.filters import Command

from app.bot.bot import bot
from app.bot.scheduler import scheduler
from app.database.user.models import users

from app.filters.role_filters import AdminFilter

router = Router()


# TODO: Проверить что работа с UTC
@router.message(Command("turn_on_advertising"), AdminFilter())
async def turn_on_advertising_handler(message: types.Message):
    scheduler.add_job(func=advert, trigger='interval', seconds=20, id="advert")
    # scheduler.add_job(func=advert, trigger='date', next_run_time=datetime.datetime.utcnow() + datetime.timedelta(hours=3, seconds=120))
    await message.answer(text=f'Рассылка включена!!')
    await bot.send_message(chat_id=message.from_user.id, text="Купи премиум!!")


@router.message(Command("turn_of_advertising"), AdminFilter())
async def turn_on_advertising_handler(message: types.Message):
    scheduler.shutdown()
    await message.answer(text=f'Рассылка выключена!!')


async def advert():
    for user in users:
        await bot.send_message(chat_id=user.id, text="Купи премиум!!")


@router.message(Command("turn_on"), AdminFilter())
async def turn_on_advertising_handler(message: types.Message):
    from arq import create_pool
    import asyncio
    from app.bot.settings import bot_settings
    from arq.connections import RedisSettings
    REDIS_SETTINGS = RedisSettings(
        host="redis",
        password=bot_settings.REDIS_PASSWORD,
        port=6379,
        database=7
    )
    await bot.send_message(chat_id=bot_settings.ADMIN, text="Ну я уже хз")
    await asyncio.sleep(10)
    arq_redis = await create_pool(REDIS_SETTINGS)
    await asyncio.sleep(10)
    job = await arq_redis.enqueue_job("download_content", _job_id="1", text="Так так так")
    await asyncio.sleep(10)
    await bot.send_message(chat_id=bot_settings.ADMIN, text=f'{(await job.status())}')
