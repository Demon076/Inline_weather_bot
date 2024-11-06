import emoji
from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.database.user.models import User
from app.keyboards.inline import WeatherCallbackFactory
from app.services.weather.api_weatherapi.get_weather_by_coordinates import get_weather_by_coordinates

router = Router()


@router.callback_query(WeatherCallbackFactory.filter(F.action == "location_current"))
async def current_weather_call(
        callback: CallbackQuery
):
    user = User.get_by_id_or_create(callback.from_user)
    weather = await get_weather_by_coordinates(
        latitude=user.location[0],
        longitude=user.location[1]
    )
    await callback.bot.edit_message_reply_markup()
    await callback.bot.edit_message_text(
        inline_message_id=callback.inline_message_id,
        text=f'*В заданном вами местоположении*{emoji.emojize("🗺")}\n\n'
             f'{weather.rus_string()}',
        parse_mode="Markdown"
    )
