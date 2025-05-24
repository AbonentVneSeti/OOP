from dataclasses import dataclass, field
from typing import Protocol, Sequence, TypeVar, Optional
import os, pickle

@dataclass
class User:
    id: int
    name: str
    login: str
    password: str = field(repr=False)
    email: str = None
    address: str = None

    def __lt__(self, other):
        return self.name < other.name

T = TypeVar('T')

class IDataRepository(Protocol[T]):
    def get_all(self) -> Sequence[T]: ...
    def get_by_id(self, id: int) -> Optional[T]: ...
    def add(self, item: T) -> None: ...
    def update(self, item: T) -> None: ...
    def delete(self, item: T) -> None: ...

class IUserRepository(IDataRepository[User], Protocol):
    def get_by_login(self, login: str) -> Optional[User]: ...

class PickleSerializer:
    @staticmethod
    def serialize(data):
        return pickle.dumps(data)

    @staticmethod
    def deserialize(data_bytes):
        return pickle.loads(data_bytes)

class DataRepository(IDataRepository[T]):
    def __init__(self, filename: str, serializer):
        self.filename = filename
        self.serializer = serializer

    def _load_data(self) -> list[T]:
        try:
            with open(self.filename, 'rb') as f:
                return self.serializer.deserialize(f.read())
        except FileNotFoundError:
            return []

    def _save_data(self, data: list[T]):
        with open(self.filename, 'wb') as f:
            f.write(self.serializer.serialize(data))

    def get_all(self) -> Sequence[T]:
        return self._load_data()

    def get_by_id(self, id: int) -> Optional[T]:
        return next((u for u in self.get_all() if u.id == id), None)

    def add(self, item: T) -> None:
        data = self._load_data()
        data.append(item)
        self._save_data(data)

    def update(self, item: T) -> None:
        data = self._load_data()
        index = next((i for i, u in enumerate(data) if u.id == item.id), None)
        if index is not None:
            data[index] = item
            self._save_data(data)
        else:
            raise ValueError("User not found")

    def delete(self, item: T) -> None:
        data = self._load_data()
        data = [u for u in data if u.id != item.id]
        self._save_data(data)

class UserRepository(DataRepository[User], IUserRepository):
    def get_by_login(self, login: str) -> Optional[User]:
        return next((u for u in self.get_all() if u.login == login), None)

class IAuthService(Protocol):
    def sign_in(self, user: User) -> None: ...
    def sign_out(self) -> None: ...
    @property
    def is_authorized(self) -> bool: ...
    @property
    def current_user(self) -> User: ...

class AuthService(IAuthService):
    def __init__(self, user_repo: IUserRepository, auth_file: str):
        self._user_repo = user_repo
        self._auth_file = auth_file
        self._current_user = None
        self._load_authentication()

    def _load_authentication(self):
        try:
            with open(self._auth_file, 'r') as f:
                user_id = int(f.read())
                self._current_user = self._user_repo.get_by_id(user_id)
        except (FileNotFoundError, ValueError):
            pass

    def _save_authentication(self):
        if self._current_user:
            with open(self._auth_file, 'w') as f:
                f.write(str(self._current_user.id))
        else:
            try:
                os.remove(self._auth_file)
            except FileNotFoundError:
                pass

    def sign_in(self, user: User) -> None:
        existing = self._user_repo.get_by_login(user.login)
        if existing and existing.password == user.password:
            self._current_user = existing
            self._save_authentication()
        else:
            raise ValueError("Invalid credentials")

    def sign_out(self) -> None:
        self._current_user = None
        self._save_authentication()

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> User:
        if not self._current_user:
            raise ValueError("Not authorized")
        return self._current_user

def main():
    # Инициализация репозитория и сервиса
    user_repo = UserRepository("users.pkl", PickleSerializer())
    auth_service = AuthService(user_repo, "auth.txt")

    # Добавление пользователя
    user = User(1, "Alice", "alice", "pass", "alice@example.com")
    user_repo.add(user)

    # Авторизация
    try:
        auth_service.sign_in(User(0, "", "alice", "pass"))
        print(f"Авторизован: {auth_service.current_user}")
    except ValueError as e:
        print(e)

    # Выход и повторная авторизация
    auth_service.sign_out()
    auth_service._load_authentication()
    print("Авторизован после выхода:", auth_service.is_authorized)

if __name__ == "__main__":
    main()