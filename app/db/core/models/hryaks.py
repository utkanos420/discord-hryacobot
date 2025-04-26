from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Hryak(Base):
    __tablename__ = "hryaks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hryak_owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # связь на User
    hryak_class_id: Mapped[int] = mapped_column(ForeignKey("hryak_classes.id"))  # связь на HryakClass
    hryak_user_name: Mapped[str] = mapped_column(String, default="не указано", server_default="не указано")
    date_owned: Mapped[str] = mapped_column(String, default="не указано", server_default="не указано")

    owner = relationship("User", back_populates="hryaks")
    hryak_class = relationship("HryakClass", back_populates="hryaks")
