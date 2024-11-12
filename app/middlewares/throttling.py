from typing import Callable, Dict, Any, Awaitable
from redis.asyncio import Redis
from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Update


class ThrottlingMiddleware(BaseMiddleware):
    __redis_prefix = "throttling_user_"

    def __init__(self, redis_conn: Redis, bot: Bot, rate_limit: int = 40):
        self.redis_conn: Redis = redis_conn
        self.bot = bot
        self.rate_limit = rate_limit

    # TODO: Уменьшить количество запросов к бд
    async def set_user_requests(self, user_tg, value: int, ex: int = None):
        ttl = await self.redis_conn.ttl(name=f'{self.__redis_prefix}{user_tg.id}')
        if ttl < 0 or ttl > 60:
            ttl = 60
        if ex is not None:
            ttl = ex
        await self.redis_conn.set(name=f'{self.__redis_prefix}{user_tg.id}', value=value, ex=ttl)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            update: Update,
            data: Dict[str, Any]
    ) -> Any:
        if update.inline_query is not None:
            return await handler(update, data)

        user_tg = data['event_from_user']
        check_user = await self.redis_conn.get(name=f'{self.__redis_prefix}{user_tg.id}')
        if check_user is not None:
            check_user = int(check_user)
            if check_user > self.rate_limit:
                await self.set_user_requests(user_tg, value=-1, ex=60)
                await self.bot.send_message(
                    chat_id=user_tg.id,
                    text="Слишком много запросов, ограничиваю вас на минуту!"
                )
                return
            elif check_user == -1:
                return

            await self.set_user_requests(user_tg, check_user+1)
        else:
            await self.set_user_requests(user_tg, 1)

        return await handler(update, data)
