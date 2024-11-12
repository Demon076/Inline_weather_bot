import emoji
from aiogram import Bot
from app.bot.bot import bot
from app.bot.settings import bot_settings
from app.database.user.models import User
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import WebAppInfo
from app.services.weather.api.get_current_weather_by_coordinates import get_weather_by_coordinates
from app.workers.scheduler.scheduler import global_scheduler


async def send_weather_to_user(bot_user_id: int):
    user = await User.get_by_id(bot_user_id)

    if (user is None or
            user.sending_weather is False
            or user.location is None
            or not user.time_is_set()):
        global_scheduler.remove_job(job_id=f'schedule_weather_{bot_user_id}')
        bot_info = Bot(token=bot_settings.TOKEN_BOT_LOG)
        await bot_info.send_message(
            chat_id=bot_settings.ADMIN,
            text="Критическая ошибка при отправке погоды пользователю!"
        )
        if user is not None:
            user.sending_weather = False
            await user.save()
            await bot.send_message(chat_id=user.id, text="Что-то пошло не так, рассылка погоды выключена ((")
        return

    weather = await get_weather_by_coordinates(
        latitude=user.location[0],
        longitude=user.location[1]
    )

    if user.horoscope is None:
        await bot.send_message(
            chat_id=user.id,
            text=f'Погодка на сейчас {emoji.emojize("🥰")}\n\n'
                 f'{weather.rus_string()}'
        )
        return

    kb = [[
        InlineKeyboardButton(
            text=f'Открыть гороскоп',
            web_app=WebAppInfo(url=f"https://horo.mail.ru/prediction/{user.horoscope.value}/today/")
        )
    ]]

    await bot.send_message(
        chat_id=user.id,
        text=f'Погодка на сейчас {emoji.emojize("🥰")}\n\n'
             f'{weather.rus_string()}\n\n'
             f'Тут можете посмотреть свой гороскоп ^_^',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
    )
