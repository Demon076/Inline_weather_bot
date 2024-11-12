import emoji
from aiogram import Router, types, F
from aiogram.filters import Command

from app.database.user.models import User
from app.keyboards.base import menu_keyboard, base_kb

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(text=f'Привет, я бот для погоды {emoji.emojize("☀️☔")}\n\n'
                              f'Вы можете воспользоваться мной в любом чате. '
                              f'Введите @inline_weather_bot и потом начните писать свой город'
                              f' или нажмите кнопку под этим сообщением.\n\n'
                              f'Приятного использования!',
                         reply_markup=base_kb()
                         )


@router.message(Command("menu"))
async def menu_cmd(message: types.Message, bot_user: User):
    await message.answer(text=f'Это моё меню, тут ты можешь воспользоваться дополнительными функциями ^_^',
                         reply_markup=menu_keyboard(bot_user)
                         )


@router.callback_query(F.data == "menu")
# TODO: Возможно сделать как-то более нормально работу с коллбеком. Сейчас нужен для возвращения.
async def menu_callback(callback: types.CallbackQuery, bot_user: User):
    await callback.message.edit_text(text=f'Это моё меню, тут ты можешь воспользоваться дополнительными функциями ^_^',
                                     reply_markup=menu_keyboard(bot_user)
                                     )


@router.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(text=f'Я бот для погоды {emoji.emojize("☀️☔")}\n\n'
                              f'Вы можете воспользоваться мной в любом чате. '
                              f'Введите @inline_weather_bot и потом начните писать свой город'
                              f' или нажмите кнопку под этим сообщением.\n\n'
                              f'Бот позволяет узнать погоду:\n'
                              f'1) Погоду в данный момент\n'
                              f'2) Погоду на будущее с шагом в 3 часа\n'
                              f'3) Погоду на будущие дни\n'
                              f'(в 12 часов дня)\n'
                              f'\nЕсли вашего города нет в списке, напишите об этом боту и возможно город добавят.\n\n'
                              f'Приятного использования!',

                         reply_markup=base_kb()
                         )
