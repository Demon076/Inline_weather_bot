from aiogram import Router, F

from app.handlers.weather.location import weather_in_location, remember_location


def location_router() -> Router:
    router = Router()
    router.include_routers(
        weather_in_location.router,
        remember_location.router
    )
    router.message.filter(F.chat.type == "private")
    router.callback_query.filter(F.message.chat.type == "private")
    return router
