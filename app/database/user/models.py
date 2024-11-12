import time
from copy import copy

import orjson

from datetime import timedelta
from typing import Tuple, Optional

from app.database.core.arq_redis import ArqRedisConnection
from app.database.core.redis import redis_conn
from app.database.user.enums import ZodiacSign


# TODO: Возможно это суперкласс, и от него слишком много зависит? Наследование может добавить или что-то такое
class User:
    id: int
    sending_weather: bool = False
    _location: Tuple[float, float] | None = None  # TODO: Переписать, чтобы местоположение хранилось более удобно
    horoscope: ZodiacSign = None
    _timezone: int | None = None
    hours: int = None
    minutes: int = None
    captcha_passed: bool = False  # TODO: Возможно не лучшее место для хранения данных о капче
    banned: bool = False

    __redis_prefix: str = "bot_user"

    @property
    def timezone(self) -> int:
        return self._timezone

    @property
    def location(self) -> Tuple[float, float]:
        return self._location

    # TODO: Переписать ошибки на английский!
    @location.setter
    def location(self, value: Tuple[float, float]):
        if value is None:
            self._location = value
            return

        if not isinstance(value, tuple):
            raise ValueError(f"location это Tuple[float, float]")

        if len(value) != 2:
            raise ValueError("Размер tuple для location может быть только 2")

        self._location = value

    @timezone.setter
    def timezone(self, value: int):
        if value is None:
            self._timezone = value
            return

        if 12 < value or value < -12:
            raise ValueError(f"Такая временная зона не поддерживается: {value}")
        self._timezone = value

    def __init__(
            self,
            id: int,
            sending_weather: bool = False,
            location: Tuple[float, float] = None,
            horoscope: ZodiacSign = None,
            timezone: int = None,
            hours: int = None,
            minutes: int = None,
            captcha_passed: bool = False,
            banned: bool = False
    ):
        self.id = id
        self.sending_weather = sending_weather
        self.location = location
        self.horoscope = horoscope
        self.timezone = timezone
        self.hours = hours
        self.minutes = minutes
        self.captcha_passed = captcha_passed
        self.banned = banned

    def time_is_set(self) -> bool:
        return self._timezone is not None and self.hours is not None and self.minutes is not None

    def time_for_user(self) -> timedelta:
        time = timedelta(hours=self.hours, minutes=self.minutes) + timedelta(hours=self._timezone)
        time = timedelta(seconds=time.seconds)  # TODO: Переделать работу со временем
        return time

    def to_json(self) -> str:
        user_dict = copy(self.__dict__)
        if user_dict['horoscope'] is not None:
            user_dict['horoscope'] = user_dict['horoscope'].value
        return orjson.dumps(user_dict).decode("utf-8")

    @staticmethod
    def from_json(json_text: str | bytes) -> 'User':
        json_load = orjson.loads(json_text)

        if not isinstance(json_load, dict):
            raise ValueError(f"Неверный json!!")

        location = json_load['_location']
        if location is not None:
            location = tuple(location)

        horoscope = json_load['horoscope']
        if horoscope is not None:
            horoscope = ZodiacSign(horoscope)

        return User(
            id=json_load['id'],
            sending_weather=json_load['sending_weather'],
            location=location,
            horoscope=horoscope,
            timezone=json_load['_timezone'],
            hours=json_load['hours'],
            minutes=json_load['minutes'],
            captcha_passed=json_load['captcha_passed'],
            banned=json_load['banned']
        )

    async def start_send_weather(self):
        await ArqRedisConnection.arq_redis.enqueue_job(
            function="start_send_weather",
            user=self
        )
        self.sending_weather = True
        await self.save()

    # TODO: Добавить дополнительные проверки успешного завершения задачи
    async def stop_send_weather(self):
        await ArqRedisConnection.arq_redis.enqueue_job(
            function="stop_send_weather",
            user=self
        )
        self.sending_weather = False
        await self.save()

    async def save(self):
        await self._save_to_redis()

    @classmethod
    async def get_by_id(cls, tg_user_id: int) -> Optional['User']:
        user = await cls._load_from_redis(tg_user_id)
        return user

    async def _save_to_redis(self):
        await redis_conn.set(
            name=f'{self.__redis_prefix}_{self.id}',
            value=self.to_json()
        )

    @classmethod
    async def _load_from_redis(cls, id: int) -> Optional['User']:
        redis_answer = await redis_conn.get(name=f'{cls.__redis_prefix}_{id}')
        if redis_answer is None:
            return redis_answer

        user = cls.from_json(redis_answer)
        return user

    async def delete(self) -> bool:
        result = await redis_conn.delete(f'{self.__redis_prefix}_{self.id}')
        return True if result == 1 else False


if __name__ == "__main__":
    user = User(
        id=123,
        sending_weather=False,
        location=(1, 2),
        horoscope=ZodiacSign.RAM,
        timezone=12,
        hours=None,
        minutes=None,
        banned=False
    )
    print(user)
    json_str = user.to_json()
    print(json_str)
    print(User.from_json(json_str))

    results = []
    users = [
        User(
            id=i,
            sending_weather=False,
            location=(1, 2),
            horoscope=ZodiacSign.RAM,
            timezone=12,
            hours=None,
            minutes=None,
            banned=False
        )
        for i in range(100000)
    ]
    start = time.perf_counter()
    for user in users:
        json_str = user.to_json()
        results.append(User.from_json(json_str))

    print(time.perf_counter() - start)
