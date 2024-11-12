import asyncio
import time

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import WebAppInfo
from redis import asyncio as aioredis

from app.bot.settings import bot_settings
from app.database.core.redis import redis_conn
from app.database.user.enums import ZodiacSign
from app.database.user.models import User
from app.filters.role_filters import AdminFilter

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


@router.message(Command("user"), AdminFilter())
async def location_handler(message: types.Message):
    user = User(
        id=123,
        sending_weather=False,
        location=(1, 2),
        horoscope=ZodiacSign.RAM,
        timezone=12,
        hours=None,
        minutes=None,
        banned=False
    )
    await message.answer(text=str(user))
    await user.save_to_redis()
    user = await User.load_from_redis(user.id)
    await message.answer(text=str(user))

    redis_conn_1: aioredis.Redis = aioredis.Redis(
        host=bot_settings.REDIS_HOST,
        port=bot_settings.REDIS_PORT,
        db=bot_settings.REDIS_DATABASE,
        password=bot_settings.REDIS_PASSWORD,
        encoding="utf-8",
        decode_responses=True,
        max_connections=1000
    )

    results = []
    users = [
        User(
            id=i,
            sending_weather=False,
            location=(1, 2),
            horoscope=ZodiacSign.RAM,
            timezone=12,
            hours=None,
            minutes=None,
            banned=False
        )
        for i in range(10000)
    ]
    start = time.perf_counter()

    async with asyncio.TaskGroup() as tg:
        for i in range(10000):
            tg.create_task(redis_conn_1.set(str(i), str(i)))
            results.append(tg.create_task(redis_conn_1.get(str(i))))

    await message.answer(text=str(time.perf_counter() - start))
