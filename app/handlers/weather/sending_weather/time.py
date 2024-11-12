from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database.user.models import User
from app.handlers.weather.sending_weather.menu import sending_weather_menu_message, sending_weather_menu_call
from app.keyboards.sending_weather import SendingWeatherMenuCallbackFactory
from aiogram.fsm.state import StatesGroup, State


class TimeRememberState(StatesGroup):
    send_timezone = State()
    send_scheduled_dispatch_time = State()


router = Router()


def time_validation(text: str) -> bool:
    if not text.find(":"):
        return False

    list_text = text.split(":")
    if len(list_text) > 2:
        return False

    if not (list_text[0].isdigit() and 0 <= int(list_text[0]) <= 24):
        return False

    if not (list_text[1].isdigit() and 0 <= int(list_text[1]) <= 60):
        return False

    return True


@router.callback_query(SendingWeatherMenuCallbackFactory.filter(F.action == "time"))
async def sending_weather_time_call(
        callback: CallbackQuery,
        callback_data: SendingWeatherMenuCallbackFactory,
        state: FSMContext
):
    await callback.message.answer(f'Хорошо давайте настроим время отправки погоды!\n'
                                  f'Напишите свою временную зону в формате от -12 до 12 целым числом')
    await state.set_state(TimeRememberState.send_timezone)

    await callback.answer()


@router.message(TimeRememberState.send_timezone)
async def location_handler(
        message: types.Message,
        state: FSMContext,
        bot_user: User
):
    if (message.text is not None
            and message.text.isdigit()
            and -12 <= int(message.text) <= 12):
        bot_user.timezone = int(message.text)
        await bot_user.save()
        await message.answer(text=f'Теперь отправьте время в которое отправлять рассылку в формате 24 часа'
                                  f' HH:MM')
        await state.set_state(TimeRememberState.send_scheduled_dispatch_time)
    else:
        await message.answer(text=f'Вы не отправили верные данные, чтобы попробовать снова нажмите кнопку меню!!')
        await state.clear()


@router.message(TimeRememberState.send_scheduled_dispatch_time)
async def location_handler(
        message: types.Message,
        state: FSMContext,
        bot_user: User
):
    if message.text is not None and time_validation(message.text):
        time = message.text.split(":")
        bot_user.hours = int(time[0]) - bot_user.timezone
        if bot_user.hours > 24:
            bot_user.hours -= 24
        elif bot_user.hours < 0:
            bot_user.hours += 24  # TODO: Переделать эту логику
        bot_user.minutes = int(time[1])
        await bot_user.save()
        await message.answer(text=f'Отлично время запомнено!')
        await sending_weather_menu_message(message, bot_user)
    else:
        await message.answer(text=f'Вы не отправили верные данные, чтобы попробовать снова нажмите кнопку меню!!')

    await state.clear()


@router.callback_query(SendingWeatherMenuCallbackFactory.filter(F.action == "forget_time"))
async def forget_location_call(
        callback: CallbackQuery,
        callback_data: SendingWeatherMenuCallbackFactory,
        bot_user: User
):
    bot_user.timezone = 0  # TODO: Переделать обнуление
    bot_user.hours = None
    bot_user.minutes = None

    if bot_user.sending_weather is False:
        await callback.message.answer(f'Заданное время удалено!')
    else:
        await bot_user.stop_send_weather()
        await callback.message.answer(f'Заданное время удалено!\n'
                                      f'Рассылка погоды выключена!!')
    await bot_user.save()
    await sending_weather_menu_call(callback, bot_user)
    await callback.answer()
