from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from app.services.weather.Weather import Weather


@dataclass
class FutureWeather:
    list_weather: List[Weather] = None

    @staticmethod
    def json_to_future_weather_list(json_future_weather: dict) -> 'FutureWeather':
        future_weather = FutureWeather()
        future_weather.list_weather = []
        for weather_id in range(int(json_future_weather['cnt'])):
            json_weather = json_future_weather['list'][weather_id]
            weather = Weather.json_to_weather(json_weather)
            future_weather.list_weather.append(weather)
        return future_weather

    def future_hour(self, time_zone: int = 0) -> List[Weather]:
        dt = datetime.utcnow() + timedelta(hours=time_zone)
        filtered_weather_list = filter(lambda o: dt < o.date, self.list_weather)
        answer = list(filtered_weather_list)[0:4]
        return answer

    def future_day(self) -> List[Weather]:
        hours = 12
        answer = [weather for weather in self.list_weather[1:] if weather.date.hour == hours]
        return answer
