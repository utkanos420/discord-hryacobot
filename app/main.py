import asyncio
import os, sys

import discord
from discord.ext import commands

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.core.models.db_helper import db_helper
from db.core.models.base import Base
from api import router as api_router

from configs.config import bot_settings

from loguru import logger
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from utils import setup_logging

logger = setup_logging()
logger.critical("Ахуеть?")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router, prefix="/hryaki")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=bot_settings.discord_bot_prefix, intents=intents)


async def load_cogs(bot: commands.Bot) -> None:
    try:
        await bot.load_extension("bot.cogs.register")
        logger.info("Коги успешно загружены")
    except Exception as e:
        logger.error(f"Ошибка загрузки когов: {e}")


async def start_db() -> None:
    try:
        async with db_helper.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("База данных инициализирована")
    except Exception as e:
        logger.error(f"Ошибка инициализации БД: {e}")


@bot.event
async def on_ready() -> None:
    """Событие запуска бота"""
    logger.info(f"Бот {bot.user} готов (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="/help"))


async def main() -> None:
    """Основная функция запуска"""
    await start_db()
    await load_cogs(bot)

    config = uvicorn.Config(
    app=app,
    port=8000,
    log_level="debug",
    log_config=None
)

    server = uvicorn.Server(config)

    try:
        await asyncio.gather(
            server.serve(),
            bot.start(bot_settings.discord_bot_token),
        )
    except discord.errors.PrivilegedIntentsRequired:
        logger.critical(
            "Бот требует привилегированных интентов, которые не включены в Discord Developer Portal. "
            "Перейди по ссылке: https://discord.com/developers/applications"
        )
    except Exception as e:
        logger.critical(f"Ошибка запуска бота или сервера: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен вручную")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")
