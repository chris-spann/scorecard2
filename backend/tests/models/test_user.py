from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


@pytest.mark.asyncio
async def test_user_model(event_loop, db: AsyncSession):
    user = User(id=uuid4(), email="test@example.com", hashed_password="1234")
    db.add(user)
    await db.commit()
    assert user.id
