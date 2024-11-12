import emoji
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.database.user.models import User

from app.handlers.weather.sending_weather.menu import sending_weather_menu_call

from app.keyboards.sending_weather import SendingWeatherMenuCallbackFactory, return_keyboard
from aiogram.fsm.state import StatesGroup, State


class LocationState(StatesGroup):
    send_location = State()
    send_location_remember = State()


router = Router()


@router.callback_query(SendingWeatherMenuCallbackFactory.filter(F.action == "turn_on"))
async def sending_weather_turn_on_call(
        callback: CallbackQuery,
        callback_data: SendingWeatherMenuCallbackFactory,
        bot_user: User
):
    if bot_user.location is not None and bot_user.time_is_set():
        await bot_user.start_send_weather()
        await sending_weather_menu_call(callback, bot_user)
    else:
        await callback.message.edit_text(text=f'Время и геопозиция не заданы, чтобы включить отправку по времени!',
                                         reply_markup=return_keyboard())

    await callback.answer()


@router.callback_query(SendingWeatherMenuCallbackFactory.filter(F.action == "turn_off"))
async def sending_weather_turn_off_call(
        callback: CallbackQuery,
        callback_data: SendingWeatherMenuCallbackFactory,
        bot_user: User
):
    await bot_user.stop_send_weather()
    await sending_weather_menu_call(callback, bot_user)
    await callback.answer()
