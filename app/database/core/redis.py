from redis import asyncio as aioredis
from app.bot.settings import bot_settings

redis_conn: aioredis.Redis = aioredis.Redis(
    host=bot_settings.REDIS_HOST,
    port=bot_settings.REDIS_PORT,
    db=bot_settings.REDIS_DATABASE,
    password=bot_settings.REDIS_PASSWORD,
    encoding="utf-8",
    decode_responses=True
)


