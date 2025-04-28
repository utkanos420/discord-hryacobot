from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class BotSettings(BaseConfig):

    discord_bot_token: str = "xxx"

    discord_bot_prefix: str = "!"

bot_settings = BotSettings()