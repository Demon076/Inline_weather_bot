import asyncio
from typing import List

from aiogram import Bot


class BotLogger:
    def __init__(self, token: str, name: str = "bot_logging"):
        self.bot = Bot(token=token)
        self.name: str = name

        self.log_queue = []
        self.log_queue_str = ""
        self.__is_waiting = False

        self.bot_users: List[int] = []

    @property
    def is_waiting(self) -> bool:
        return self.__is_waiting

    async def log(self, text: str):
        self.log_queue.append(text)
        self.log_queue_str += text
        await self._lazy_log()

    async def _lazy_log(self):
        if len(self.log_queue) >= 5:
            self.__is_waiting = False
            await self._send_log(self.log_queue)
            self.log_queue = []
        elif self.is_waiting:
            pass
        else:
            self.__is_waiting = True
            await asyncio.sleep(60)
            if not self.__is_waiting:
                return
            self.__is_waiting = False
            await self._send_log(self.log_queue)
            self.log_queue = []

    async def _send_log(self, text: str | list[str]):
        if isinstance(text, str):
            await self.bot.send_message(chat_id=5731946909, text=text)
            await self.bot.session.close()
        else:
            text_from_list = ""
            for i in text:
                text_from_list += i
            await self.bot.send_message(chat_id=5731946909, text=text_from_list)
            await self.bot.session.close()
