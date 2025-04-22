from discord.ext import commands
from db.db_methods.register_method import register_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.db_config import settings
import logging

logger = logging.getLogger(__name__)

from db.core.models.db_helper import db_helper

class Register(commands.Cog):
    """Cog для регистрации пользователей"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        await ctx.send("Регистрируем вас в бюро свинопасов: свинуслуги")

        async for session in db_helper.session_dependency():
            try:
                user = await register_user(session=session, discord_id=ctx.author.id, swineherd_class="сельский свинопас", user_level=1, has_active_key=True)
                if user:
                    await ctx.send(f"Пользователь {ctx.author} успешно зарегистрирован!")
                else:
                    await ctx.send(f"Ошибка регистрации пользователя {ctx.author}.")
            except Exception as e:
                await ctx.send(f"Ошибка: {e}")
                logger.error(f"Ошибка при регистрации пользователя: {e}")

async def setup(bot):
    await bot.add_cog(Register(bot))
