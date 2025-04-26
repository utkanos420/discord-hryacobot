import logging

from discord import File, Embed
from discord.ext import commands

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy.future import select

from db.db_config import settings
from db.db_methods.register_method import register_user
from db.core.models import basic_classes, HryakClass
from db.core.models.db_helper import db_helper


logger = logging.getLogger(__name__)


# Временно эта функция вынесена тут, так как не реализована базовая апишка, классы хряков вставляются на лету после первого !register
async def insert_basic_classes(session: Session, basic_classes):
    result = await session.execute(select(HryakClass))
    if not result.scalars().all():
        session.add_all(basic_classes)
        await session.commit()


# В будущем этот класс будет упрощен, пока все крутится вокруг него
class Register(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    # при развертке бота устанавливается префикс "!", получается команда "!register"
    @commands.command(name="register")
    async def register(self, ctx):

        async for session in db_helper.session_dependency():
            try:
                user = await register_user(session=session, discord_id=ctx.author.id, swineherd_class="сельский свинопас", user_level=1, has_active_key=True)
                if user:
                    await insert_basic_classes(session, basic_classes)
                    
                    file = File("../assets/bot/hryaki/hryak_documents.png")
                    e = Embed()
                    e.set_image(url="attachment://hryak_documents.png")
                    # пока так, мне не нравится - некрасиво
                    await ctx.send(file=file, embed=e, content="**Добро пожаловать, SEO-свинопас!**\n"
                                                               "\n"
                                                               "Готовы получить своего первого хряка?\n")
                else:
                    await ctx.send(f"Ошибка регистрации пользователя {ctx.author}.")
            except Exception as e:
                await ctx.send(f"Ошибка: {e}")
                logger.error(f"Ошибка при регистрации пользователя: {e}")


async def setup(bot):
    await bot.add_cog(Register(bot))
