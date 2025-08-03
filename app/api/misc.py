from fastapi import APIRouter
from sqlalchemy import text

from app.core.db import SessionDep

misc_router = APIRouter(prefix="/misc")

@misc_router.get("/healthcheck")
async def healthcheck(session: SessionDep):
    await session.execute(text("SELECT 1;"))
    return

