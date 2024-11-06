from aiogram import Router

from app.filters.role_filters import AdminFilter
from app.handlers.admin.city import delete, setting, add, info, json, old


def city_router() -> Router:
    router = Router()
    router.include_routers(add.router, delete.router, info.router, json.router, old.router, setting.router)
    router.message.filter(AdminFilter())
    router.callback_query.filter(AdminFilter())
    router.inline_query.filter(AdminFilter())
    return router
