from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.database.user.enums import ZodiacSign
from app.database.user.models import User

from app.handlers.weather.sending_weather.menu import sending_weather_menu_call
from app.keyboards.horoscope import HoroscopeCallbackFactory, horoscope_keyboard

from app.keyboards.sending_weather import SendingWeatherMenuCallbackFactory
router = Router()


@router.callback_query(SendingWeatherMenuCallbackFactory.filter(F.action == "horoscope"))
async def sending_weather_turn_on_call(
        callback: CallbackQuery,
        callback_data: SendingWeatherMenuCallbackFactory
):
    user = User.get_by_id_or_create(callback.from_user)
    await callback.message.edit_text(text=f'Задайте знак зодиака, если хотите вместе'
                                          f' с погодой получать рассылку гороскопа!',
                                     reply_markup=horoscope_keyboard(user))
    await callback.answer()


@router.callback_query(HoroscopeCallbackFactory.filter(F.zodiac_sign != "delete"))
async def sending_weather_turn_on_call(
        callback: CallbackQuery,
        callback_data: HoroscopeCallbackFactory
):
    user = User.get_by_id_or_create(callback.from_user)
    user.horoscope = ZodiacSign(callback_data.zodiac_sign)
    await sending_weather_menu_call(callback)
    await callback.answer()


@router.callback_query(HoroscopeCallbackFactory.filter(F.zodiac_sign == "delete"))
async def sending_weather_turn_on_call(
        callback: CallbackQuery,
        callback_data: HoroscopeCallbackFactory
):
    user = User.get_by_id_or_create(callback.from_user)
    user.horoscope = None
    await sending_weather_menu_call(callback)
    await callback.answer()
