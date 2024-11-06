from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, Message, InlineQuery, CallbackQuery

from app.database.user.models import User
from app.handlers.capcha import capcha_cmd


# TODO: ОбЪеденить с новым пользователем и переделать чтобы капча была не только на message

class CapchaMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: Dict[str, Any]
    ) -> Any:
        if not User.user_exists(message.from_user.id):
            return await capcha_cmd(message)
        return await handler(message, data)
