import requests


def get_weather(lat, lon):
    # URL API wttr.in
    base_url = "http://wttr.in/"

    # Формирование URL запроса
    url = f"{base_url}{lat},{lon}?format=j1"

    try:
        # Отправка GET-запроса
        response = requests.get(url)

        # Проверка статуса ответа
        if response.status_code == 200:
            # Декодирование JSON-ответа
            weather_data = response.json()

            # Вывод результата
            print("Прогноз погоды:")
            print(weather_data['current_condition']['description'])
            print(f"Температура: {weather_data['current_condition']['temp']}")
            print(f"Влажность: {weather_data['current_condition']['humidity']}%")
        else:
            print(f"Ошибка при получении данных: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")


# Пример использования
get_weather(55.7558, 37.6173)  # Москва