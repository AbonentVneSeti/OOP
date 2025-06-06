from typing import Protocol
import os
from user_repository import IUserRepository
from user import User

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
