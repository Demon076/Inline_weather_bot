import emoji
from app.bot.bot import bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import WebAppInfo
from app.services.weather.api_weatherapi.get_weather_by_coordinates import get_weather_by_coordinates


async def send_weather(user: 'User'):
    from app.database.user.models import User
    user: User
    weather = await get_weather_by_coordinates(
        latitude=user.location[0],
        longitude=user.location[1]
    )
    await bot.send_message(
        chat_id=user.id,
        text=f'Погодка на сейчас {emoji.emojize("🥰")}\n\n'
             f'{weather.rus_string()}'
    )

    if user.horoscope is not None:
        kb = [[
            InlineKeyboardButton(
                text=f'Открыть гороскоп',
                web_app=WebAppInfo(url=f"https://horo.mail.ru/prediction/{user.horoscope.value}/today/")
            )
        ]]
        await bot.send_message(
            chat_id=user.id,
            text=f'Тут можете посмотреть свой гороскоп ^_^',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
        )
