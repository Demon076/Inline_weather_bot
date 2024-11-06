from typing import List

import emoji
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from app.keyboards.inline import city_keyboard
from app.services.weather.data import Cities


class DefaultResults:
    __default_results: List[InlineQueryResultArticle] = []
    not_found = [InlineQueryResultArticle(
        id="1",
        title="Не могу найти город в соих списках",
        description="Если вашего города не нашлось, то напишите об этом боту в лс.",
        input_message_content=InputTextMessageContent(
            message_text=f'Ваш город не найден {emoji.emojize("😢")}\n\n'
                         f'Напишите боту, чтобы ваш населённый пункт добавили в списки!'
        )
    )]

    @classmethod
    def reload_default_results(cls):
        cls.__default_results = []
        for index, city in enumerate(Cities.list_cities_ru):
            cls.__default_results.append(
                InlineQueryResultArticle(
                    id=str(index),
                    title=city,
                    description="Показать погоду!",
                    input_message_content=InputTextMessageContent(
                        message_text=f'Нажмите на кнопку ниже, чтобы узнать погоду в городе {city} ^_^'
                    ),
                    reply_markup=city_keyboard(Cities.dict_cities_ru[city].id)
                )
            )

    @classmethod
    def default_results(cls):
        if cls.__default_results:
            return cls.__default_results
        cls.reload_default_results()
        return cls.__default_results
