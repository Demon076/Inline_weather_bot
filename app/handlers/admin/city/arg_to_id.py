from app.services.weather.data import Cities


def arg_to_id(arg: str) -> int | None:
    city_id = None
    if arg in Cities.dict_cities_ru:
        city_id = Cities.dict_cities_ru[arg].id
    elif arg in Cities.dict_cities_en:
        city_id = Cities.dict_cities_en[arg].id
    elif arg.isnumeric() and int(arg) in Cities.dict_cities_id:
        city_id = int(arg)

    return city_id
