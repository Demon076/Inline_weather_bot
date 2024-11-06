from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    TOKEN: str
    ADMIN: int
    WEATHER: str
    TOKEN_BOT_LOG: str
    ADMIN_BOT_LOG: int
    APIKEY_WEATHERAPI: str


bot_settings = BotSettings()

if __name__ == "__main__":
    print(bot_settings.TOKEN)
