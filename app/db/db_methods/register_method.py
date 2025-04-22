from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from db.core.models import User
from uuid import uuid4


async def register_user(session: AsyncSession,
                        discord_id: int,
                        swineherd_class: str = "сельский свинопас",
                        user_level: int = 1,
                        has_active_key: bool = False):
    try:
        new_user = User(
            discord_id=discord_id,
            swineherd_class=swineherd_class,
            user_level=user_level,
            has_active_key=has_active_key
        )
        
        session.add(new_user)
        await session.commit()
        
        return new_user
    
    except IntegrityError:
        await session.rollback()
        print(f"Ошибка: пользователь с Discord ID {discord_id} уже существует.")
        return None
    except Exception as e:
        await session.rollback()
        print(f"Произошла ошибка при регистрации: {e}")
        return None

