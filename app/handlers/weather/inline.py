from copy import copy

import emoji

from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from app.database.user.models import User
from app.handlers.weather.default_results import DefaultResults
from app.keyboards.inline import city_keyboard
from app.keyboards.inline_location import inline_location_keyboard
from app.services.weather.api_weatherapi.get_weather_by_coordinates import get_weather_by_coordinates
from app.services.weather.data import Cities

router = Router()


@router.inline_query()
async def show_city_weather(inline_query: InlineQuery):
    results = DefaultResults.default_results()
    if inline_query.query != "":
        list_cities = Cities.search_in_list(inline_query.query)
        if list_cities:
            results = []
            for index, city in enumerate(list_cities):
                results.append(
                    InlineQueryResultArticle(
                        id=str(index),
                        title=city,
                        description="Показать погоду!",
                        input_message_content=InputTextMessageContent(
                            message_text=f'Нажмите на кнопку ниже, чтобы узнать погоду в городе {city} ^_^',
                        ),
                        reply_markup=city_keyboard(Cities.dict_cities_ru[city].id)
                    )
                )
        else:
            results = DefaultResults.not_found

    user = User.get_by_id_or_create(inline_query.from_user)
    results = copy(results)

    if user.location is not None:
        # TODO: Написать кэширование через Redis чтобы не запрашивалась погода чаще, чем раз в полчаса в одной точке
        weather = await get_weather_by_coordinates(
            latitude=user.location[0],
            longitude=user.location[1]
        )
        results.insert(0, InlineQueryResultArticle(
            id="location",
            title="Погода в заданном местоположении",
            description="Показывает погоду в местоположении, которое вы задали в боте",
            input_message_content=InputTextMessageContent(
                message_text=f'*В заданном вами местоположении*{emoji.emojize("🗺")}\n\n'
                             f'{weather.rus_string()}',
                parse_mode="Markdown"
            )
        ))
    else:
        results.insert(0, InlineQueryResultArticle(
            id="location",
            title="Погода в заданном местоположении",
            description="Вы можете задать местоположение в боте, чтобы смотреть там погоду",
            input_message_content=InputTextMessageContent(
                message_text=f'Сначала настройте эту функцию в боте!!'
            )
        ))

    await inline_query.answer(results, is_personal=True, cache_time=0)
