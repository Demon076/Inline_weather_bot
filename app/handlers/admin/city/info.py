from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from app.handlers.admin.city.arg_to_id import arg_to_id
from app.services.weather.data import Cities

router = Router()


@router.message(Command("info_city"))
async def info_city_cmd(message: types.Message, command: CommandObject):
    if not command.args:
        await message.answer("Введите русское или английское название города!!")
        return
    else:
        city_id = arg_to_id(command.args)

        if city_id is None:
            await message.answer("Не могу найти город в списке!!")
            return
        city = Cities.dict_cities_id[city_id]

        await message.answer(text=city.rus_string())
