from enum import Enum
from typing import Tuple, List, Dict


class ZodiacSign(Enum):
    # Овен (Aries)
    RAM = "Aries"
    # Телец (Taurus)
    BULL = "Taurus"
    # Близнецы (Gemini)
    TWINS = "Gemini"
    # Рак (Cancer)
    CRAB = "Cancer"
    # Лев (Leo)
    LION = "Leo"
    # Дева (Virgo)
    MAIDEN = "Virgo"
    # Весы (Libra)
    SCALES = "Libra"
    # Скорпион (Scorpio)
    SCORPION = "Scorpio"
    # Стрелец (Sagittarius)
    ARCHER = "Sagittarius"
    # Козерог (Capricorn)
    GOAT = "Capricorn"
    # Водолей (Aquarius)
    WATER_BEARER = "Aquarius"
    # Рыбы (Pisces)
    FISH = "Pisces"

    @staticmethod
    def list_zodiac_signs() -> List['ZodiacSign']:
        return ZodiacSignHelp.list_zodiac_signs()

    def russian_name(self) -> str:
        return ZodiacSignHelp.russian_name(self)


class ZodiacSignHelp: # TODO: Сделать подклассом енума
    _zodiac_rus_names: Dict[str, str] = {
        "Aries": "овен",
        "Taurus": "телец",
        "Gemini": "близнецы",
        "Cancer": "рак",
        "Leo": "лев",
        "Virgo": "дева",
        "Libra": "весы",
        "Scorpio": "скорпион",
        "Sagittarius": "стрелец",
        "Capricorn": "козерог",
        "Aquarius": "водолей",
        "Pisces": "рыбы"
    }

    _list_zodiac_signs: List[ZodiacSign] = None

    @classmethod
    def list_zodiac_signs(cls) -> List[ZodiacSign]:
        if cls._list_zodiac_signs is None:
            cls._list_zodiac_signs = [ZodiacSign(en_sign_name) for en_sign_name in list(cls._zodiac_rus_names.keys())]

        return cls._list_zodiac_signs

    @classmethod
    def russian_name(cls, sign: ZodiacSign) -> str:
        return cls._zodiac_rus_names[sign.value].capitalize()
