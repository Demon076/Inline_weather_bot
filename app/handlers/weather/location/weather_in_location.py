import emoji
from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.keyboards.base import MenuCallbackFactory
from app.keyboards.location import LocationCallbackFactory
from app.services.weather.api.get_current_weather_by_coordinates import get_weather_by_coordinates
from aiogram.fsm.state import StatesGroup, State


class LocationState(StatesGroup):
    send_location = State()
    send_location_remember = State()


router = Router()


@router.callback_query(MenuCallbackFactory.filter(F.action == "location_weather"))
async def location_weather_call(
        callback: CallbackQuery,
        callback_data: LocationCallbackFactory,
        state: FSMContext
):
    await callback.message.answer(f'Хорошо, отправьте геолокацию, прикрепив её к сообщению телеграмм!')
    await callback.answer()
    await state.set_state(LocationState.send_location)


@router.message(LocationState.send_location)
async def location_handler(
        message: types.Message,
        state: FSMContext
):
    if message.location is not None:
        latitude = message.location.latitude
        longitude = message.location.longitude

        weather = await get_weather_by_coordinates(latitude, longitude)
        await message.answer(f'*В этом местоположении*{emoji.emojize("🗺")}\n\n'
                             f'{weather.rus_string()}',
                             parse_mode="Markdown"
                             )

    else:
        await message.answer(text=f'Вы не отправили геолокацию, чтобы попробовать снова нажмите кнопку меню!!')

    await state.clear()
