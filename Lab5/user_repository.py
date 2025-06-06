from typing import Protocol, Optional
from data_repository import IDataRepository,DataRepository
from user import User


class IUserRepository(IDataRepository[User], Protocol):
    def get_by_login(self, login: str) -> Optional[User]:
        pass


class UserRepository(DataRepository[User], IUserRepository):
    def get_by_login(self, login: str) -> Optional[User]:
        return next((user for user in self.get_all() if user.login == login), None)