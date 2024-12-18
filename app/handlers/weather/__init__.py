from aiogram import Router

from app.handlers.weather import inline, callback_inline, location, sending_weather
from app.handlers.weather.location import location_router


# TODO: Запоминать город пользователя, чтобы не искать
def weather_router() -> Router:
    router = Router()
    router.include_routers(
        inline.router,
        callback_inline.router,
        location_router(),
        sending_weather.sending_weather_router()
    )
    return router
