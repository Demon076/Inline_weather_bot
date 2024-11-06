from aiogram import Router, types
from aiogram.filters import Command
from aiogram.filters.command import CommandObject

from app.handlers.admin.city.arg_to_id import arg_to_id
from app.handlers.admin.city.json import json_cities_cmd

from app.handlers.weather.default_results import DefaultResults
from app.services.weather.data import Cities

router = Router()


@router.message(Command("delete_city"))
async def delete_city_cmd(message: types.Message, command: CommandObject):
    city_id = arg_to_id(command.args)

    if city_id is None:
        await message.answer(text="Такого города нет в моём списке!!")
    else:
        try:
            city = Cities.delete_city(city_id)
            await message.answer(text=city.rus_string())

            DefaultResults.reload_default_results()
            await json_cities_cmd(message)
        except Exception as ex:
            await message.answer(text="Что-то пошло не так при удалении!")
