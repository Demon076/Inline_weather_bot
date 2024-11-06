from aiohttp import ClientSession

from app.bot.settings import bot_settings
from app.services.weather.city import City


# TODO: Переделать api в единый класс?
async def get_city(
        city_name: str,
        state_code: str = "",
        country_code: str = "",
        limit: int = -1,
        add_local_names: bool = False
) -> City:
    client_session = ClientSession()
    async with client_session as session:
        url = 'https://api.openweathermap.org/geo/1.0/direct'
        params = {'q': f'{city_name}', 'appid': bot_settings.WEATHER}
        async with session.get(url=url, params=params) as response:
            cities_json = await response.json()
            city_json = cities_json[0]
            city = City(
                name_en=city_json['local_names']['en'],
                name_ru=city_json['local_names']['ru'],
                lat=city_json['lat'],
                lon=city_json['lon'],
                country_code=city_json['country'],
                state_code=city_json['state'],
                local_names=city_json['local_names'] if add_local_names else None
            )
            return city
