# from aiogram import Router, types
# from aiogram.filters import Command
# #
# from app.services.weather.api.get_weather_future import get_weather_future
# from app.services.weather.data import Cities
#
# router = Router()
#
#
# @router.message(Command("weather_future"))
# async def weather_future_cmd(message: types.Message):
#     city = Cities.dict_cities_en['Moscow']
#     future_weather = await get_weather_future(lat=city.lat, lon=city.lon)
#     str_weather = ""
#     for weather in future_weather.list_weather:
#         str_weather = str_weather + weather.rus_string() + "\n"
#     await message.answer(str_weather[:4050])

if __name__ == "__main__":
    pass
