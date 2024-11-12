from app.bot.settings import bot_settings
from app.services.weather.Weather import Weather
from aiohttp import ClientSession


def json_to_weather(weather_json: dict) -> 'Weather':
    weather = Weather(
        temp=round(weather_json['current']['temp_c'], 1),
        temp_feels_like=round(weather_json['current']['feelslike_c'], 1),
        weather_main=weather_json['current']['condition']['text'],
        wind_speed=round((weather_json['current']['wind_kph'] * 1000) / 3600, 2)
    )

    if 'dt_txt' in weather_json:
        weather.date = Weather.str_to_date(weather_json['dt_txt'])

    return weather


async def get_weather_coordinates(latitude: float, longitude: float) -> Weather:
    coordinates = f'{latitude}, {longitude}'

    client_session = ClientSession()
    async with client_session as session:
        url = "http://api.weatherapi.com/v1/current.json"
        params = {
            "key": bot_settings.APIKEY_WEATHERAPI,
            "q": coordinates,
        }

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            weather = json_to_weather(weather_json)
            return weather
