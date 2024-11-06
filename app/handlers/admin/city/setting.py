from typing import List

from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from app.handlers.admin.city.arg_to_id import arg_to_id
from app.handlers.admin.city.info import info_city_cmd
from app.handlers.admin.city.json import json_cities_cmd
from app.handlers.weather.default_results import DefaultResults
from app.services.weather.data import Cities

router = Router()


@router.message(Command("setting_city"))
async def setting_city_cmd(message: types.Message, command: CommandObject):
    try:
        parse = command.args.split(",")
        parse = [str(i).strip() for i in parse]
        city_id = arg_to_id(parse[0])

        if city_id is None:
            await message.answer(text="Не могу настроить город, так как не найдено id!!")
            return

        await setting_city(message, parse, city_id)
        await json_cities_cmd(message)
    except Exception as ex:
        await message.answer(f'Что-то пошло не так при настройке!!\n{ex}')


# TODO: Переделать добавление и удаление\удаление апдейт
async def setting_city(message: types.Message, parse: List[str], city_id: int):
    city = Cities.dict_cities_id[city_id]
    Cities.delete_city(city_id)

    if len(parse[1]) != 0:
        rus_name = parse[1]
        city.name_ru = rus_name
    if len(parse[2]) != 3:
        time_zone = 0
        if not parse[2].isnumeric() or int(parse[2]) not in range(-12, 13):
            await message.answer(text="Временная зона невалидна, установлена на нулевую!!")
        else:
            time_zone = int(parse[2])
        city.time_zone = time_zone

    await Cities.add_city(city)
    DefaultResults.reload_default_results()

    await info_city_cmd(message=message, command=CommandObject(args=city.name_en))
    await info_city_cmd(message=message, command=CommandObject(args=city.name_ru))
    await info_city_cmd(message=message, command=CommandObject(args=str(city.id)))
