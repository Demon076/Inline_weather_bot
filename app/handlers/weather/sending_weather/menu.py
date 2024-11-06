from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.database.user.models import User
from app.keyboards.base import MenuCallbackFactory
from app.keyboards.sending_weather import menu_keyboard

router = Router()


def text_sending_weather_menu(user: User):
    location = "Местоположение не задано"
    if user.location is not None:
        location = user.location

    time = "Время отправки не задано"
    if user.time_is_set():
        time = str(user.time_for_user())

    horoscope = "Гороскоп не задан"
    if user.horoscope is not None:
        horoscope = user.horoscope.russian_name()

    text = (f'Здесь вы можете настроить рассылку погоды в заданное время!!\n\n'
            f'Сейчас рассылка погоды: {"Включена" if user.sending_weather else "Выключена"}\n'
            f'Заданное местоположение: {location}\n'
            f'Время отправки: {time}\n'
            f'Гороскоп: {horoscope}')

    return text


@router.callback_query(MenuCallbackFactory.filter(F.action == "sending_weather"))
async def sending_weather_menu_call(
        callback: CallbackQuery
):
    user = User.get_by_id_or_create(callback.from_user)
    await callback.message.edit_text(
        text=text_sending_weather_menu(user),
        reply_markup=menu_keyboard(user=user)
    )
    await callback.answer()


async def sending_weather_menu_message(
        message: Message
):
    user = User.get_by_id_or_create(message.from_user)
    await message.answer(
        text=text_sending_weather_menu(user),
        reply_markup=menu_keyboard(user=user)
    )