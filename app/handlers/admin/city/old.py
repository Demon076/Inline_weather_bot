from aiogram import types, Router
from aiogram.filters import Command, CommandObject

from app.services.weather.api_openweathermap.get_city import get_city
from app.services.weather.city import City

router = Router()


@router.message(Command("city_coordinates"))
async def weather_cmd(message: types.Message, command: CommandObject):
    try:
        city: City = await get_city(command.args)
        await message.answer(text=str(city))
    except Exception:
        await message.answer("Напиши город, пажазя ^_^")
