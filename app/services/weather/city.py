from dataclasses import dataclass


class CityUniqueId:
    __counter = 56

    @classmethod
    def set_counter(cls, counter: int):
        cls.__counter = counter

    @classmethod
    def new_id(cls) -> int:
        cls.__counter += 1
        return cls.__counter


@dataclass
class City:
    id: int = -1
    name_en: str = ""
    name_ru: str = ""
    lat: float = 0
    lon: float = 0
    time_zone: int = 0
    country_code: str = ""
    state_code: str = ""
    local_names: dict = None

    def rus_string(self) -> str:
        return (f'Город: {self.name_ru}\n'
                f'Английское название: {self.name_en}\n'
                f'Код страны: {self.country_code}\n'
                f'Стейт код: {self.state_code}\n'
                f'Временная зона: {self.time_zone}\n'
                f'Координаты:\n'
                f'lat={self.lat}\n'
                f'lon={self.lon}\n'
                f'\nid сейчас = {self.id}')
