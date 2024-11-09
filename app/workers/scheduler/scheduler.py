from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore

from app.bot.settings import bot_settings


def setup_scheduler() -> AsyncIOScheduler:
    redis_job_store = RedisJobStore(
        jobs_key="scheduler_jobs",
        run_times_key="scheduler_run_times_key",
        db=bot_settings.REDIS_DATABASE,
        host=bot_settings.REDIS_HOST,
        port=bot_settings.REDIS_PORT,
        password=bot_settings.REDIS_PASSWORD
    )
    jobstores = {
        'default': redis_job_store
    }
    scheduler = AsyncIOScheduler(
        timezone='UTC',
        jobstores=jobstores
    )
    return scheduler
