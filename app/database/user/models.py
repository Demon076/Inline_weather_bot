from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Tuple, List, Dict
from aiogram.types import User as Telegram_User

from app.bot.scheduler import scheduler
from app.database.user.enums import ZodiacSign
from app.database.user.services import send_weather

users: List['User'] = []


@dataclass
class User:
    id: int
    sending_weather: bool = False
    location: Tuple[float, float] = None  # TODO: Переписать, чтобы местоположение хранилось более удобно
    horoscope: ZodiacSign = None
    _timezone: int = None
    hours: int = None
    minutes: int = None
    banned: bool = False

    @property
    def timezone(self) -> int:
        return self._timezone

    @timezone.setter
    def timezone(self, value: int):
        if 12 < value < -12:
            raise ValueError(f"Такая временная зона не поддерживается: {value}")
        self._timezone = value

    @staticmethod
    def user_exists(tg_user_id: int):
        for user in users:
            if user.id == tg_user_id:
                return True

        return False

    @staticmethod
    def get_by_id_or_create(tg_user: Telegram_User) -> 'User':
        # TODO: Возможно переделать сделав create отдельно
        #  сделать запрос только по id
        for user in users:
            if user.id == tg_user.id:
                return user

        user = User(id=tg_user.id)
        users.append(user)

        return user

    def time_is_set(self):
        return self._timezone is not None and self.hours is not None and self.minutes is not None

    def time_for_user(self) -> timedelta:
        time = timedelta(hours=self.hours, minutes=self.minutes) + timedelta(hours=self._timezone)
        time = timedelta(seconds=time.seconds)  # TODO: Переделать работу со временем
        return time

    def start_send_weather(self):
        scheduler.add_job(
            func=send_weather,
            trigger='cron',
            hour=self.hours,
            minute=self.minutes,
            start_date=datetime.now(timezone.utc),
            id=f'scheduler_{self.id}',
            kwargs={
                'user': self
            }
        )
        self.sending_weather = True

    def stop_send_weather(self):
        scheduler.remove_job(job_id=f'scheduler_{self.id}')
        self.sending_weather = False


if __name__ == "__main__":
    f = ZodiacSign.RAM.value
    print(f)
