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
        callback_data: SendingWeatherMenuCallbackFactory,
        bot_user: User
):
    await callback.message.edit_text(text=f'Задайте знак зодиака, если хотите вместе'
                                          f' с погодой получать рассылку гороскопа!',
                                     reply_markup=horoscope_keyboard(bot_user))
    await callback.answer()


@router.callback_query(HoroscopeCallbackFactory.filter(F.zodiac_sign != "delete"))
async def sending_weather_turn_on_call(
        callback: CallbackQuery,
        callback_data: HoroscopeCallbackFactory,
        bot_user: User
):
    bot_user.horoscope = ZodiacSign(callback_data.zodiac_sign)
    await bot_user.save()
    await sending_weather_menu_call(callback, bot_user)
    await callback.answer()


@router.callback_query(HoroscopeCallbackFactory.filter(F.zodiac_sign == "delete"))
async def sending_weather_turn_on_call(
        callback: CallbackQuery,
        callback_data: HoroscopeCallbackFactory,
        bot_user: User
):
    bot_user.horoscope = None
    await bot_user.save()
    await sending_weather_menu_call(callback, bot_user)
    await callback.answer()
