from typing import Any

from fastapi import Depends, Response
from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from app.deps.db import CurrentAsyncSession
from app.deps.users import CurrentSuperuser
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/users")


@router.get("", response_model=Page[UserRead])
async def get_paginated_users(user: CurrentSuperuser, session: CurrentAsyncSession, response: Response) -> Any:
    query = select(User).order_by(User.created)
    response.headers["Content-Range"] = "users 0-9/100"
    return await paginate(session, query)
