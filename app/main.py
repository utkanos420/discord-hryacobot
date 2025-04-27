import asyncio
import logging
import os

import discord
from discord.ext import commands

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.core.models.db_helper import db_helper
from db.core.models.base import Base
from api import router as api_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

bot = commands.Bot(command_prefix="!", intents=intents)


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

    # Асинхронный запуск FastAPI
    config = uvicorn.Config(app=app, port=8000, log_level="debug")
    server = uvicorn.Server(config)

    token = ""
    try:
        await asyncio.gather(
            server.serve(),
            bot.start(token),
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
