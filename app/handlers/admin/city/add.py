from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from app.handlers.admin.city.json import json_cities_cmd
from app.handlers.admin.city.setting import setting_city
from app.services.weather.data import Cities

router = Router()


@router.message(Command("add_city"))
async def add_city_cmd(message: types.Message, command: CommandObject):
    try:
        parse = command.args.split(",")
        parse = [str(i).strip() for i in parse]
        name_city = parse[0]

        city = await Cities.add_city_api_str(name_city=name_city)
        await message.answer(text="Город добавлен!")
        await setting_city(message, parse, city.id)

        await json_cities_cmd(message)
    except Exception as ex:
        await message.answer(f"Что-то пошло не так при добавлении!!!\n{ex}")
