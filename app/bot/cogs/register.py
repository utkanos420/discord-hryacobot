import logging
import discord
from discord import File, Embed
from discord.ext import commands
from discord.ui import Button, View

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy.future import select

from db.db_config import settings
from db.db_methods.register_method import register_user
from db.core.models import basic_classes, HryakClass
from db.core.models.db_helper import db_helper

from api.v1.crud import get_hryak_by_user_id, get_hrayks_by_user_id
from bot.cogs.patterns.chances import generate_drop


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

                    button = Button(label="Получить хряка!", style=discord.ButtonStyle.blurple)

                    async def button_callback(interaction):
                        res = generate_drop()
                        if res["hryak_type"] == "common":
                            await ctx.send("Обычный хряк - тоже неплохо!")
                        elif res["hryak_type"] == "uncommon":
                            await ctx.send("Кому-то сегодня везет!")

                    button.callback = button_callback

                    view = View()
                    view.add_item(button)

                    await ctx.send(file=file, embed=e, content="**Добро пожаловать, SEO-свинопас!**\n"
                                                               "\n"
                                                               "Готовы получить своего первого хряка?\n", view=view)
                else:
                    await ctx.send(f"Ошибка регистрации пользователя {ctx.author}.")
            except Exception as e:
                await ctx.send(f"Ошибка: {e}")
                logger.error(f"Ошибка при регистрации пользователя: {e}")

    @commands.command(name="хряки")
    async def show_all_hryaks(self, ctx):
        async for session in db_helper.session_dependency():
            hryaks = await get_hrayks_by_user_id(session=session, owner_id=ctx.author.id)

            file = File("../assets/bot/hryaki/detective_hryak.png")
            e = Embed()
            e.set_image(url="attachment://detective_hryak.png")

            if hryaks:
                button = Button(label="Показать хряков", style=discord.ButtonStyle.blurple)
                
                async def button_callback(interaction):
                    messages = []
                    for hryak in hryaks:
                        messages.append(f"Хряк: {hryak.hryak_user_name}, ID: {hryak.id}, Владелец: {hryak.hryak_owner_id}")
    
                    await interaction.response.send_message("\n".join(messages), ephemeral=True)

                button.callback = button_callback
                
                view = View()
                view.add_item(button)

                await ctx.send(file=file, embed=e, content="Нажмите кнопку ниже, чтобы увидеть ваших хряков", view=view)
            else:
                await ctx.send("Нет хряков в базе.")


async def setup(bot):
    await bot.add_cog(Register(bot))
