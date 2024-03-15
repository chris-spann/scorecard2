from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class TestUserModel:
    async def test_user_model(self, db: AsyncSession):
        user = User(id=uuid4(), email=f"test{uuid4()}@example.com", hashed_password="1234")
        db.add(user)
        await db.commit()
        assert user.id

    def test_user_repr(self):
        user_id = uuid4()
        user_email = "test@example.com"
        user = User(id=user_id, email=user_email)

        result = repr(user)

        assert result == f"User(id={user_id!r}, name={user_email!r})"
