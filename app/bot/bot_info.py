from app.bot.bot import bot
from app.bot.settings import bot_settings
from app.middlewares.bot_info.BotInfo import BotInfo

bot_info: BotInfo = BotInfo(
    bot_info_token=bot_settings.TOKEN_BOT_LOG,
    admin=bot_settings.ADMIN_BOT_LOG
)
bot_info.set_bot_title(bot)
