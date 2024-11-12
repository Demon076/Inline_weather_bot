from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from app.database.user.models import User


router = Router()


# TODO: Доделать фильтр к этому

@router.message(Command("delete"))
async def ban_cmd(message: types.Message, command: CommandObject):
    try:
        bot_user: User = await User.get_by_id(tg_user_id=int(command.args))
        res = await bot_user.delete()
        if res:
            await message.answer(text="Пользователь удалён!")
        else:
            await message.answer(text="Пользователя не удалось удалить!")
    except Exception as ex:
        await message.answer(f"Что-то пошло не так при удалении!!!\n{ex}")
