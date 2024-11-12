import json
from pathlib import PurePath
from typing import List

from app.services.weather.api_openweathermap.get_city import get_city
from app.services.weather.city import City, CityUniqueId
from app.utils.root_dir import root_path


class Cities:
    path: PurePath = root_path() / "resources/weather/cities.json"
    dict_cities_id: dict = {}
    dict_cities_ru: dict = {}
    dict_cities_en: dict = {}
    list_cities_ru: List[str] = []
    list_cities_en: List[str] = []

    @classmethod
    def load_cities(cls):
        with open(cls.path, 'r') as file:
            dict_cities = json.load(file)

        for key, city in dict_cities.items():
            city = City(**city)
            city.id = CityUniqueId.new_id()
            cls.dict_cities_id[city.id] = city
            cls.dict_cities_ru[city.name_ru] = city
            cls.dict_cities_en[city.name_en] = city
            cls.list_cities_ru.append(city.name_ru)
            cls.list_cities_en.append(city.name_en)

        cls.list_cities_ru.sort()
        cls.list_cities_en.sort()

    @classmethod
    def save_json(cls):
        with open(cls.path, 'w') as file:
            file.write(json.dumps(cls.dict_cities_ru, default=lambda o: o.__dict__, indent=4))

    @classmethod
    async def add_city_api_str(cls, name_city: str) -> City:
        city = await get_city(name_city)
        return await cls.add_city(city)

    @classmethod
    async def add_city(cls, city: City) -> City:
        city.id = CityUniqueId.new_id()
        cls.dict_cities_id[city.id] = city
        cls.dict_cities_ru[city.name_ru] = city
        cls.dict_cities_en[city.name_en] = city
        if city.name_ru not in cls.list_cities_ru:
            cls.list_cities_ru.append(city.name_ru)
            cls.list_cities_ru.sort()
        if city.name_en not in cls.list_cities_en:
            cls.list_cities_en.append(city.name_en)
            cls.list_cities_en.sort()

        cls.save_json()
        return city

    @classmethod
    def delete_city(cls, city_id: int) -> City:
        city = cls.dict_cities_id.pop(city_id)
        cls.dict_cities_en.pop(city.name_en)
        cls.dict_cities_ru.pop(city.name_ru)
        index = cls.list_cities_en.index(city.name_en)
        cls.list_cities_en.pop(index)
        index = cls.list_cities_ru.index(city.name_ru)
        cls.list_cities_ru.pop(index)
        cls.save_json()
        return city

    @classmethod
    def search_in_list(cls, text: str) -> List[str]:  # TODO: Исправить работу с английским текстом
        res = []
        for city in cls.list_cities_ru:
            if text in city:
                res.append(city)
        res.sort(key=lambda x: x.startswith(text), reverse=True)
        return res


if __name__ == "__main__":
    Cities.load_cities()
    print(id(Cities.dict_cities_ru['Москва']))
    print(id(Cities.dict_cities_id[57]))
