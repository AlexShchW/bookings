import pytest

from app.users.dao import UsersDAO


@pytest.mark.parametrize(
    "id,email,exists",
    [
        (1, "test@test.com", True),
        (2, "sasha@example.com", True),
        (777, "absent@example.com", False),
    ],
)
async def test_find_user_by_id(id: int, email: str, exists: bool):
    user = await UsersDAO.find_by_id(id)
    if exists:
        assert user
        assert user.id == id
        assert user.email == email
    else:
        assert user is None
