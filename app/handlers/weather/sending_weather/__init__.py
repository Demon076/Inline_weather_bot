from aiogram import Router, F

from app.handlers.weather.sending_weather import menu, switching, time, horoscope


def sending_weather_router() -> Router:
    router = Router()
    router.include_routers(
        menu.router,
        switching.router,
        time.router,
        horoscope.router
    )
    router.message.filter(F.chat.type == "private")
    router.callback_query.filter(F.message.chat.type == "private")
    return router
