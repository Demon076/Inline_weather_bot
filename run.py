import asyncio

from app.bot.bot import bot_setup, bot
from app.bot.dispatcher import dp, registration_dispatcher
from app.bot.log import start_logging
from app.bot.scheduler import scheduler
from app.services.weather.data import Cities


async def main():
    await bot_setup(bot)
    start_logging()
    Cities.load_cities()
    registration_dispatcher(dp)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
