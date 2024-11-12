from copy import copy
import pickle
import emoji

from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from redis.asyncio import Redis

from app.bot.settings import bot_settings
from app.database.user.models import User
from app.handlers.weather.default_results import DefaultResults
from app.keyboards.inline import city_keyboard
from app.services.weather.Weather import Weather
from app.services.weather.api.get_current_weather_by_coordinates import get_weather_by_coordinates
from app.services.weather.data import Cities

router = Router()


# TODO: Переделать на другой ключ и хеш
async def cached_weather_for_user(bot_user: User) -> Weather:
    redis: Redis = Redis(
        host=bot_settings.REDIS_HOST,
        port=bot_settings.REDIS_PORT,
        db=bot_settings.REDIS_DATABASE,
        password=bot_settings.REDIS_PASSWORD,
    )

    weather = await redis.get(
        name=f"cached_weather_for_user_{bot_user.id}_{bot_user.location[0]}_{bot_user.location[1]}"
    )
    if weather is None:
        weather = await get_weather_by_coordinates(
            latitude=bot_user.location[0],
            longitude=bot_user.location[1]
        )
        await redis.set(
            name=f"cached_weather_for_user_{bot_user.id}_{bot_user.location[0]}_{bot_user.location[1]}",
            value=pickle.dumps(weather),
            ex=60*10
        )
    else:
        weather = pickle.loads(weather)

    await redis.close()

    return weather


async def result_for_user(
        bot_user: User,
        results: list[InlineQueryResultArticle]
) -> list[InlineQueryResultArticle]:
    results = copy(results)

    if bot_user.location is not None:
        weather = await cached_weather_for_user(bot_user)
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

    return results


@router.inline_query()
async def show_city_weather(inline_query: InlineQuery, bot_user: User):
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

    results = await result_for_user(bot_user, results)

    await inline_query.answer(results, is_personal=True, cache_time=0)
