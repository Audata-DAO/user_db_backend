from fastapi import APIRouter

from app.domains.users.routes import users_router

main_router = APIRouter(prefix="/api")

main_router.include_router(users_router)
