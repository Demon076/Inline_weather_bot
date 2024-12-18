import asyncio
import logging
from typing import Callable, Dict, Any, Awaitable, List, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, Message, InlineQuery, CallbackQuery

from app.bot.bot import bot
from app.bot.settings import bot_settings
from app.database.user.models import User
from app.middlewares.bot_info.BotInfo import BotInfo
from app.middlewares.bot_info.update_to_str import general_to_str


class NewUserMiddleware(BaseMiddleware):
    def __init__(self, bot_info: Optional[BotInfo] = None):
        self.bot_info = bot_info
        self.users: List[int] = []

    async def create_log(self, obj: Message | CallbackQuery | InlineQuery):
        log = self.bot_info.bot_title + "\n\n"
        log += 'Новый пользователь в этой сессии:\n'
        log += general_to_str(obj)
        log += f'Type update: {obj.__class__.__name__}\n'
        return log

    async def send_new_user(self, update: Update):
        obj = None
        if update.message is not None:
            obj = update.message
        elif update.callback_query is not None:
            obj = update.callback_query
        elif update.inline_query is not None:
            obj = update.inline_query

        if obj is None:
            return

        if obj.from_user.id not in self.users:
            log = await self.create_log(obj)
            logging.info(log)
            self.users.append(obj.from_user.id)
            if self.bot_info is not None:
                await self.bot_info.send_partial(self.bot_info.bot.send_message, text=log)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            update: Update,
            data: Dict[str, Any]
    ) -> Any:
        asyncio.create_task(self.send_new_user(update))  # TODO: Переделать через дату

        user_tg = data['event_from_user']
        bot_user = await User.get_by_id(user_tg.id)
        if bot_user is None:
            bot_user = User(id=user_tg.id)
            await bot_user.save()
        data['bot_user'] = bot_user

        # TODO: Добавить логгирование для забаненных
        if bot_user.banned:
            return

        return await handler(update, data)
