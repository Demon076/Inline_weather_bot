import requests


def get_weather(api_key, coordinates):
    base_url = 'https://api.openweathermap.org/data/2.5/weather?lat=55.7558&lon=37.6173&APPID=d439373ea464a43d05de075e91862944'
    params = {'lat': 57.6263877, 'lon': 39.8933705, 'APPID': 'd439373ea464a43d05de075e91862944'}
    response = requests.get(base_url)

    weather_data = response.json()
    return weather_data


# Пример использования
api_key = "705eb74ccfd74d4695f213257241910"
coordinates = "55.7558,37.6173"  # Координаты Нью-Йорка

weather_info = get_weather(api_key, coordinates)
print(weather_info)
