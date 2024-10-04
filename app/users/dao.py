from app.base_dao.base_dao import BaseDAO
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users
