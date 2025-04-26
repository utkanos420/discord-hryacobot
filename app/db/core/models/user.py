from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    discord_id: Mapped[int] = mapped_column(Integer, unique=True)
    swineherd_class: Mapped[str] = mapped_column(String, default="сельский свинопас", server_default="сельский свинопас")
    user_level: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    user_xp: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    has_active_key: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")

    hryaks = relationship("Hryak", back_populates="owner")
