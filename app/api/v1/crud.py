from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from db.core.models import Hryak

from .schemas import (HryakCreate,
                      HryakBase,
                      HryakUpdate,
                      HryakBaseUpdatePartial)


async def get_hryaks(session: AsyncSession):
    stmt = select(Hryak).order_by(Hryak.id)
    result: Result = await session.execute(statement=stmt)
    hryaks = result.scalars().all()
    return list(hryaks)


async def get_hryak(session: AsyncSession, hryak_id: str):
    return await session.get(Hryak, hryak_id)


async def get_hryak_by_user_id(session: AsyncSession, owner_id: str):
    stmt = select(Hryak).where(Hryak.hryak_owner_id == owner_id)
    result = await session.execute(stmt)
    hryak = result.scalar_one_or_none()
    return hryak


async def get_hrayks_by_user_id(session: AsyncSession, owner_id: str):
    stmt = select(Hryak).order_by(Hryak.id)
    result = await session.execute(stmt)
    hryaks = result.scalars().all()
    return hryaks


async def create_hryak(session: AsyncSession, hryak_in: HryakCreate) -> Hryak:
    hryak = Hryak(**hryak_in.model_dump())
    session.add(hryak)
    await session.commit()
    return (hryak)


async def update_hryak(
        session: AsyncSession,
        hryak: Hryak,
        hryak_update: HryakBaseUpdatePartial,
        partial: bool = True
) -> Hryak:
    for name, value in hryak_update.model_dump(exclude_unset=partial).items():
        setattr(hryak, name, value)

    print(f"Updating hryak {hryak.id} with {hryak_update}")

    session.add(hryak)

    await session.commit()
    await session.refresh(hryak)

    return hryak


async def delete_hryak(session: AsyncSession, hryak_in: Hryak) -> None:
    await session.delete(hryak_in)
    await session.commit()
    return None
    