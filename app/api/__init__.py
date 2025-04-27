from fastapi import APIRouter

from .v1.views import crud_router


router = APIRouter()
router.include_router(crud_router)
