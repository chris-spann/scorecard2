from typing import Any

from fastapi import APIRouter, HTTPException, Response
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from app.deps.db import CurrentAsyncSession
from app.deps.users import CurrentUser
from app.models.item import Item
from app.schemas.item import Item as ItemSchema
from app.schemas.item import ItemCreate, ItemUpdate

router = APIRouter(prefix="/items")


@router.get("", response_model=Page[ItemSchema])
async def get_paginated_items(response: Response, session: CurrentAsyncSession, user: CurrentUser) -> Any:
    query = select(Item).filter(Item.user_id == user.id)
    page = await paginate(session, query)
    response.headers["Content-Range"] = "items 0-9/100"
    return page


@router.post("", response_model=ItemSchema, status_code=201)
async def create_item(
    item_in: ItemCreate,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    item = Item(**item_in.dict())
    item.user_id = user.id
    session.add(item)
    await session.commit()
    return item


@router.put("/{item_id}", response_model=ItemSchema)
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    item: Item | None = await session.get(Item, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(404)
    update_data = item_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    session.add(item)
    await session.commit()
    return item


@router.get("/{item_id}", response_model=ItemSchema)
async def get_item(
    item_id: int,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    item: Item | None = await session.get(Item, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(404)
    return item


@router.delete("/{item_id}")
async def delete_item(item_id: int, session: CurrentAsyncSession, user: CurrentUser) -> Any:
    item: Item | None = await session.get(Item, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(404)
    await session.delete(item)
    await session.commit()
    return {"success": True}
