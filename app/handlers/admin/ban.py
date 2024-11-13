from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from app.database.user.models import User

router = Router()


@router.message(Command("ban"))
async def ban_cmd(message: types.Message, command: CommandObject):
    try:
        user = await User.get_by_id(tg_user_id=int(command.args))
        user.banned = True
        await user.save()
        await message.answer(text="Пользователь забанен!")
    except Exception as ex:
        await message.answer(f"Что-то пошло не так при добавлении!!!\n{ex}")


@router.message(Command("unban"))
async def ban_cmd(message: types.Message, command: CommandObject):
    try:
        user = await User.get_by_id(tg_user_id=int(command.args))
        user.banned = False
        await user.save()
        await message.answer(text="Пользователь разбанен!")

    except Exception as ex:
        await message.answer(f"Что-то пошло не так при добавлении!!!\n{ex}")
