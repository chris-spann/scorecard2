from typing import Any

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.deps.db import get_async_session
from app.deps.users import CurrentSuperuser
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/users")


@router.get("", response_model=Page[UserRead])
async def get_paginated_users(
    user: CurrentSuperuser,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    query = select(User).order_by(User.created)
    return await paginate(session, query)
