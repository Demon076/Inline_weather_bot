import json
from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from app.utils.root_dir import root_path

main_weather_dict: Dict[str, str] = json.load(fp=open(root_path() / "resources/weather/main_weather_dict.json", 'r'))


@dataclass
class Weather:
    temp: float = 0
    temp_feels_like: float = 0
    weather_main: str = ""
    wind_speed: float = 0
    date: datetime = None
    weather_json = None

    @staticmethod
    def str_to_date(date_str: str) -> datetime:
        date: datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date

    @staticmethod
    def json_to_weather(weather_json: dict) -> 'Weather':
        weather = Weather(
            temp=round(weather_json['main']['temp'] - 273.15, 0),
            temp_feels_like=round(weather_json['main']['feels_like'] - 273.15, 0),
            weather_main=weather_json['weather'][0]['main'],
            wind_speed=round(weather_json['wind']['speed'], 2)
        )

        if 'dt_txt' in weather_json:
            weather.date = Weather.str_to_date(weather_json['dt_txt'])

        return weather

    def rus_string(self):
        if self.weather_main in main_weather_dict:
            weather_main = main_weather_dict[self.weather_main]
        else:
            weather_main = self.weather_main

        answer = (f'Погода: {weather_main}\n'
                  f'Температура: {int(self.temp)}°C\n'
                  f'Ощущается, как: {int(self.temp_feels_like)}°C\n'
                  f'Скорость ветра: {self.wind_speed} м/с')
        return answer
