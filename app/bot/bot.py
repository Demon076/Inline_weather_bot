from aiogram import Bot
from aiogram.types import BotCommand

from app.bot.settings import bot_settings

bot = Bot(token=bot_settings.TOKEN)

bot_title = None


# 6661684613:AAHD310i858LnVi3yfJ4Gi6LlCLnY-fiICw

async def bot_setup(aiogram_bot: Bot) -> None:
    await aiogram_bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Запуск бота"),
            BotCommand(command="menu", description="Дополнительный функционал бота"),
            BotCommand(command="help", description="Полезная информация о боте")
        ]
    )


async def stop_bot(aiogram_bot: Bot):
    await aiogram_bot.close()