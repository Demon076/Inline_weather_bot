from aiogram import Router

from app.filters.role_filters import AdminFilter
from app.handlers.admin import log, admin_help, user_management, ban
from app.handlers.admin.city import city_router


def admin_router() -> Router:
    router = Router()
    router.include_routers(
        city_router(),
        admin_help.router,
        ban.router,
        log.router,
        user_management.router
    )
    router.message.filter(AdminFilter())
    router.callback_query.filter(AdminFilter())
    router.inline_query.filter(AdminFilter())
    return router
