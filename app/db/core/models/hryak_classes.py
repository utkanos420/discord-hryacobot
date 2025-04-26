from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class HryakClass(Base):
    __tablename__ = "hryak_classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hryak_class: Mapped[str] = mapped_column(String, default="не указано", server_default="не указано")
    hryak_rank: Mapped[str] = mapped_column(String, default="обычная", server_default="обычная")
    hryak_description: Mapped[str] = mapped_column(String, default="не указано", server_default="не указано")
    hryak_base_weight: Mapped[float] = mapped_column(Float, default=1.0, server_default="1.0")
    hryak_base_attack: Mapped[float] = mapped_column(Float, default=100.0, server_default="100.0")
    hryak_base_health: Mapped[float] = mapped_column(Float, default=100.0, server_default="100.0")
    hryak_base_xp_growth: Mapped[float] = mapped_column(Float, default=1.0, server_default="1.0")

    hryaks = relationship("Hryak", back_populates="hryak_class")

# Пока они тут, не придумал как лучше
basic_classes = [
            HryakClass(hryak_class='Бродячий хряк', hryak_rank='common', hryak_description='Обычный хряк, который выдается при старте игры', 
                       hryak_base_weight=1.0, hryak_base_attack=5.0, hryak_base_health=50.0, 
                       hryak_base_xp_growth=1.0),
            HryakClass(hryak_class='Бывалый хряк', hryak_rank='common', hryak_description='Кажется, прошлое этого хряка окутано тайнами', 
                       hryak_base_weight=1.0, hryak_base_attack=7.0, hryak_base_health=75.0, 
                       hryak_base_xp_growth=1.1)
        ]
