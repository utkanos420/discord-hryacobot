from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from db.core.models import db_helper, Hryak

from . import crud


async def hryak_by_id(
        hryak_id: Annotated[str, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> Hryak:
    hryak = await crud.get_hryak(session=session, hryak_id=hryak_id)
    if hryak is not None:
        return hryak
    
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Хряк не найден"
    )
