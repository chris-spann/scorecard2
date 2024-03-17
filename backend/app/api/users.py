from typing import Any

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import Select
from starlette.responses import Response

from app.deps.db import CurrentAsyncSession, get_async_session
from app.deps.users import CurrentSuperuser
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter()


# @router.get("/users", response_model=list[UserRead])
# async def get_users(
#     response: Response,
#     session: CurrentAsyncSession,
#     user: CurrentSuperuser,
#     skip: int = 0,
#     limit: int = 100,
# ) -> Any:
#     total: int = (await session.scalar(select(func.count(User.id)))) or 0
#     users = (await session.execute(select(User).offset(skip).limit(limit))).fetchall()
#     response.headers["Content-Range"] = f"{skip}-{skip + len(users)}/{total}"
#     return users


@router.get("/users", response_model=Page[UserRead])
async def get_paginated_users(
    user: CurrentSuperuser,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    query = select(User).order_by(User.created)
    return await paginate(session, query)
