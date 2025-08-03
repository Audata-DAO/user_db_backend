from fastapi import APIRouter

from app.api.users import users_router
from app.api.misc import misc_router

main_router = APIRouter(prefix="/api")

main_router.include_router(misc_router)
main_router.include_router(users_router)
