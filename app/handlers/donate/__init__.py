from aiogram import Router
from app.handlers.donate import donate_cmd


def donate_router() -> Router:
    router = Router()
    router.include_routers(
        donate_cmd.router
    )
    return router
