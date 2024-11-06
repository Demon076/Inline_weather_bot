import aiogram.types
from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from app.database.user.models import User
from app.handlers.admin.city.json import json_cities_cmd
from app.handlers.admin.city.setting import setting_city
from app.services.weather.data import Cities

router = Router()


# TODO: Доделать фильтр к этому

@router.message(Command("ban"))
async def ban_cmd(message: types.Message, command: CommandObject):
    try:
        if User.user_exists(int(command.text)):
            user = User.get_by_id_or_create(
                tg_user=aiogram.types.User(
                    id=int(command.text),
                    is_bot=False,
                    first_name=""
                )
            )
            user.banned = True
            await message.answer(text="Пользователь забанен!")

    except Exception as ex:
        await message.answer(f"Что-то пошло не так при добавлении!!!\n{ex}")


@router.message(Command("unban"))
async def ban_cmd(message: types.Message, command: CommandObject):
    try:
        if User.user_exists(int(command.text)):
            user = User.get_by_id_or_create(
                tg_user=aiogram.types.User(
                    id=int(command.text),
                    is_bot=False,
                    first_name=""
                )
            )
            user.banned = False
            await message.answer(text="Пользователь разбанен!")

    except Exception as ex:
        await message.answer(f"Что-то пошло не так при добавлении!!!\n{ex}")
