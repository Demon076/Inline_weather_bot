from aiogram import Router, F
from app.handlers.donate import donate_cmd, stars


def donate_router() -> Router:
    router = Router()
    router.include_routers(
        donate_cmd.router,
        stars.router
    )
    router.message.filter(F.chat.type == "private")
    router.callback_query.filter(F.message.chat.type == "private")
    return router
