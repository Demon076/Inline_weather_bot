from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.bot.bot_info import bot_info
from app.database.core.redis import redis_conn
from app.handlers import base, capcha
from app.handlers.admin import admin_router
from app.handlers.exp import donate, premium, webapp, keys
from app.handlers.weather import weather_router
from app.middlewares.bot_info.LogMiddleware import LogMiddleware
from app.middlewares.bot_info.NewUserMiddleware import NewUserMiddleware
from app.middlewares.capcha import CapchaMiddleware
from app.utils.root_dir import root_path

dp = Dispatcher(
    storage=RedisStorage(
        redis=redis_conn
    )
)


def registration_dispatcher(dispatcher: Dispatcher) -> None:
    dispatcher.update.outer_middleware(LogMiddleware(
        bot_info=bot_info,
        path_log_file=root_path() / "log.log",
        clean_log=True,
        limit_counter=30
    ))
    dispatcher.update.outer_middleware(NewUserMiddleware(bot_info=bot_info))
    dispatcher.message.outer_middleware(CapchaMiddleware())
    dispatcher.include_routers(
        admin_router(),
        base.router,
        weather_router(),
        capcha.router,
        donate.router,
        premium.router,
        webapp.router,
        keys.router
    )

