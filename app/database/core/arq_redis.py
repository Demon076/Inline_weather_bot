from arq import create_pool
from app.bot.settings import bot_settings
from arq.connections import RedisSettings, ArqRedis


class ArqRedisConnection:
    arq_redis: ArqRedis = ArqRedis()

    # TODO: Переделать тут на более чистый код
    @classmethod
    async def arq_redis_setup(cls):
        cls.arq_redis = await create_pool(RedisSettings(
            host=bot_settings.REDIS_HOST,
            password=bot_settings.REDIS_PASSWORD,
            port=bot_settings.REDIS_PORT,
            database=bot_settings.REDIS_DATABASE
        ))
