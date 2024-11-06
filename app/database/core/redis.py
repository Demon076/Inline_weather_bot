from redis import asyncio as aioredis

from app.bot.settings import bot_settings

redis_conn = aioredis.from_url(
    "redis://redis",
    password=bot_settings.REDIS_PASSWORD,
    port=6379,
    db=0,
    encoding="utf-8",
    decode_responses=True
)

