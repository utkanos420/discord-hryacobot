from fastapi import APIRouter, HTTPException, status, Depends

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.core.models import db_helper
from . import crud
from .schemas import Hryak, HryakCreate, HryakUpdate, HryakBaseUpdatePartial


crud_router = APIRouter()


@crud_router.get("/", response_model=list[Hryak], tags=["hryaki"])
async def get_hryaks(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_hryaks(session=session)


@crud_router.post("/", response_model=Hryak, tags=["hryaki"])
async def crteate_hryak(hryak_in: HryakCreate, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.create_hryak(session=session, hryak_in=hryak_in)