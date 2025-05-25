from dataclasses import dataclass, field, asdict, is_dataclass
from typing import Protocol, Sequence, TypeVar, Optional, Self
import os, json
T = TypeVar('T')


@dataclass
class User:
    id: int
    login: str
    password: str = field(repr=False, compare=False)
    name: str = field(compare=False)
    email: Optional[str] = field(default=False, compare=False)
    address: Optional[str] = field(default=False, compare=False)

    def __lt__(self, other: Self) -> bool:
        return self.name.lower() < other.name.lower()


class IDataRepository(Protocol[T]):
    def get_all(self) -> Sequence[T]:
        pass

    def get_by_id(self, id: int) -> Optional[T]:
        pass

    def add(self, item: T) -> None:
        pass

    def update(self, item: T) -> None:
        pass

    def delete(self, item: T) -> None:
        pass


class DataRepository(IDataRepository[T]):
    def __init__(self, filename: str, serializer) -> None:
        self.filename = filename
        self.serializer = serializer

    def _load_data(self) -> list[T]:
        try:
            with open(self.filename, 'rb') as f:
                return self.serializer.deserialize(f.read())
        except FileNotFoundError:
            return []

    def _save_data(self, data: list[T]) -> None:
        with open(self.filename, 'wb') as f:
            f.write(self.serializer.serialize(data))

    def get_all(self) -> Sequence[T]:
        return self._load_data()

    def get_by_id(self, id: int) -> Optional[T]:
        return next((user for user in self.get_all() if user.id == id), None)

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
        data = [user for user in data if user.id != item.id]
        self._save_data(data)


class IUserRepository(IDataRepository[User], Protocol):
    def get_by_login(self, login: str) -> Optional[User]:
        pass


class UserRepository(DataRepository[User], IUserRepository):
    def get_by_login(self, login: str) -> Optional[User]:
        return next((user for user in self.get_all() if user.login == login), None)


class IAuthService(Protocol):
    def sign_in(self, login: str, password: str) -> None:
        pass

    def sign_out(self) -> None:
        pass

    @property
    def is_authorized(self) -> bool:
        pass

    @property
    def current_user(self) -> User:
        pass


class AuthService(IAuthService):
    def __init__(self, user_repo: IUserRepository, auth_file: str) -> None:
        self._user_repo = user_repo
        self._auth_file = auth_file
        self._current_user = None
        self._load_authentication()

    def _load_authentication(self) -> None:
        try:
            with open(self._auth_file, 'r') as f:
                user_id = int(f.read())
                self._current_user = self._user_repo.get_by_id(user_id)
        except (FileNotFoundError, ValueError):
            pass

    def _save_authentication(self) -> None:
        if self._current_user:
            with open(self._auth_file, 'w') as f:
                f.write(str(self._current_user.id))
        else:
            try:
                os.remove(self._auth_file)
            except FileNotFoundError:
                pass

    def sign_in(self, login: str, password: str) -> None:
        existing = self._user_repo.get_by_login(login)
        if existing and existing.password == password:
            self._current_user = existing
            self._save_authentication()
        else:
            raise ValueError("Неверные данные")

    def sign_out(self) -> None:
        self._current_user = None
        self._save_authentication()

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> User:
        if not self._current_user:
            raise ValueError("Не авторизован")
        return self._current_user


class JSONSerializer:
    @staticmethod
    def serialize(data: list) -> bytes:
        serializable_data = []
        for item in data:
            if is_dataclass(item):
                serializable_data.append(asdict(item))
            else:
                serializable_data.append(item)
        return json.dumps(serializable_data).encode('utf-8')

    @staticmethod
    def deserialize(data_bytes: bytes) -> list:
        if not data_bytes:
            return []
        data_json = data_bytes.decode('utf-8')
        data_list = json.loads(data_json)
        return [User(**item) for item in data_list]


def main():
    user_repo = UserRepository("users.json", JSONSerializer())
    auth_service = AuthService(user_repo, "auth.txt")

    users = [
        User(id = 0, login = "admin", password = "admin123", name = "Admin", email="Admin@admin.com"),
        User(id = 1, login = "login", password = "pass", name = "Name", email = "NameDigits@example.com", address="example street")
             ]
    for user in users:
        if not user_repo.get_by_id(user.id):
            user_repo.add(user)

    print("Авторизация с неверными данными:")
    try:
        auth_service.sign_in(login="not login",password= "not pass")
        print(f"Авторизован: {auth_service.current_user}")
    except ValueError as e:
        print(e)

    print("\nАвторизация с верными данными:")
    try:
        auth_service.sign_in(login="login",password= "pass")
        print(f"Авторизован: {auth_service.current_user}")
    except ValueError as e:
        print(e)
    auth_service.sign_out()
    print("\nАвторизован после выхода:", auth_service.is_authorized)

if __name__ == "__main__":
    main()