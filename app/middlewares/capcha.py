from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, Message, InlineQuery, CallbackQuery

from app.database.user.models import User
from app.handlers.base import start_cmd
from app.handlers.capcha import capcha_cmd


# TODO: ОбЪеденить с новым пользователем и переделать чтобы капча была не только на message

class CapchaMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: Dict[str, Any]
    ) -> Any:
        bot_user: User = data['bot_user']
        if bot_user.captcha_passed:
            return await handler(message, data)
        if message.text == "/start":
            await start_cmd(message)

        return await capcha_cmd(message)
