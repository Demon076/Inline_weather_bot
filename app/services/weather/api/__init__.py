from datetime import datetime, timedelta

from app.bot.bot import bot
from app.bot.settings import bot_settings


class RateLimiter:  # TODO: Убрать риск(доработать)
    rate_limit = 1000
    counter = 0
    date_last_update: datetime = datetime.now()

    @classmethod
    def is_limited(cls) -> bool:
        if cls.counter >= cls.rate_limit:
            if timedelta(hours=24) <= (datetime.now() - cls.date_last_update):
                cls.counter = 0
                cls.date_last_update = datetime.now()
                return False
            return True

        return False

    @classmethod
    def add_counter(cls):
        cls.counter += 1

    @classmethod
    async def request_api(cls):
        if cls.is_limited():
            await bot.send_message(chat_id=bot_settings.ADMIN, text="Запросы к боту кончились!!")
            raise Exception
        cls.add_counter()
