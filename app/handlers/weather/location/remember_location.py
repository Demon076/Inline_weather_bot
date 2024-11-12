import emoji
from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from app.database.user.models import User
from app.handlers.weather.location.weather_in_location import LocationState
from app.keyboards.base import MenuCallbackFactory
from app.keyboards.location import LocationCallbackFactory, location_keyboard
from app.keyboards.sending_weather import SendingWeatherMenuCallbackFactory
from app.services.weather.api.get_current_weather_by_coordinates import get_weather_by_coordinates

router = Router()


@router.callback_query(MenuCallbackFactory.filter(F.action == "location"))
async def remember_location_call(
        callback: CallbackQuery,
        bot_user: User
):
    await remember_location(callback, "menu", bot_user)


@router.callback_query(SendingWeatherMenuCallbackFactory.filter(F.action == "location"))
async def remember_location_call(
        callback: CallbackQuery,
        bot_user: User
):
    await remember_location(callback, MenuCallbackFactory(action="sending_weather"), bot_user)


# TODO: Сделать чтобы в фабрике местоположения передавалось,
#  кнопка вернуться и сообщение редактировалось после удаления или изменения
async def remember_location(callback: CallbackQuery, return_callback_data: str | CallbackData, bot_user: User):
    text = "Настройка местоположения:"
    if bot_user.location is not None:
        text = (f"Заданное местоположение - {bot_user.location}\n"
                f"Настройка местоположения:")
    await callback.message.edit_text(text=text,
                                     reply_markup=location_keyboard(
                                         user=bot_user,
                                         return_callback_data=return_callback_data
                                     ))
    await callback.answer()


@router.callback_query(LocationCallbackFactory.filter(F.action == "remember_location"))
async def remember_location_call(
        callback: CallbackQuery,
        callback_data: LocationCallbackFactory,
        state: FSMContext
):
    await callback.message.answer(f'Хорошо, отправьте геолокацию, прикрепив её к сообщению телеграмм и я её запомню!')
    await callback.answer()
    await state.set_state(LocationState.send_location_remember)


@router.message(LocationState.send_location_remember)
async def remember_location_handler(
        message: types.Message,
        state: FSMContext,
        bot_user: User
):
    if message.location is not None:
        latitude = message.location.latitude
        longitude = message.location.longitude

        bot_user.location = (latitude, longitude)
        await bot_user.save()

        weather = await get_weather_by_coordinates(latitude, longitude)
        await message.answer(f'*В этом местоположении*{emoji.emojize("🗺")}\n\n'
                             f'{weather.rus_string()}',
                             parse_mode="Markdown"
                             )
        await message.answer(text=f'Местоположение запомнено!!')

    else:
        await message.answer(text=f'Вы не отправили геолокацию, чтобы попробовать снова нажмите кнопку меню!!')

    await state.clear()


@router.callback_query(LocationCallbackFactory.filter(F.action == "forget_location"))
async def forget_location_call(
        callback: CallbackQuery,
        callback_data: LocationCallbackFactory,
        bot_user: User
):
    bot_user.location = None
    if bot_user.sending_weather is False:
        await callback.message.answer(f'Заданная геолокация удалена!')
    else:
        await bot_user.stop_send_weather()
        await callback.message.answer(f'Заданная геолокация удалена!\n'
                                      f'Рассылка погоды выключена!!')
    await bot_user.save()

    await callback.answer()
# TODO: Двойной вызов save()
