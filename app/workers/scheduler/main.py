import logging
from datetime import datetime, timezone

from arq.connections import RedisSettings
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.bot.settings import bot_settings
from app.database.user.models import User
from app.database.user.services import send_weather
from app.workers.scheduler.log import start_logging
from app.workers.scheduler.scheduler import setup_scheduler


# TODO: Переделать через контекст в cron_jobs
async def start_send_weather(ctx, user: User):
    scheduler: AsyncIOScheduler = ctx['scheduler']
    scheduler.add_job(
        func=send_weather,
        trigger='cron',
        hour=user.hours,
        minute=user.minutes,
        start_date=datetime.now(timezone.utc),
        id=f'schedule_weather_{user.id}',
        kwargs={
            'user': user
        }
    )
    return True


async def stop_send_weather(ctx, user: User):
    scheduler: AsyncIOScheduler = ctx['scheduler']
    scheduler.remove_job(job_id=f'schedule_weather_{user.id}')
    return True


async def startup(ctx):
    start_logging()
    ctx['scheduler'] = setup_scheduler()
    ctx['scheduler'].start()
    logging.info(msg=f'Worker start!')


async def shutdown(ctx):
    scheduler: AsyncIOScheduler = ctx['scheduler']
    scheduler.shutdown()
    logging.info(msg=f'Worker shutdown!')


class WorkerSettings:
    functions = [start_send_weather, stop_send_weather]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings(
        host=bot_settings.REDIS_HOST,
        password=bot_settings.REDIS_PASSWORD,
        port=bot_settings.REDIS_PORT,
        database=bot_settings.REDIS_DATABASE
    )
