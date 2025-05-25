from typing import List, Any, Protocol


class PropertyChangedListenerProtocol(Protocol):
    def on_property_changed(self, obj : Any, property_name: str) -> None:
        pass


class DataChangedProtocol(Protocol):
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        pass

    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        pass


class PropertyChangingListenerProtocol(Protocol):
    def on_property_changing(self, obj : Any, property_name: str, old_value : Any, new_value : Any) -> bool:
        pass


class DataChangingProtocol(Protocol):
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        pass

    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        pass


class User(DataChangingProtocol, DataChangedProtocol):
    def __init__(self) -> None:
        self._changing_listeners: List[PropertyChangingListenerProtocol] = []
        self._changed_listeners: List[PropertyChangedListenerProtocol] = []
        self._name = ""
        self._email = ""

    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        self._changing_listeners.append(listener)

    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        self._changing_listeners.remove(listener)

    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        self._changed_listeners.append(listener)

    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        self._changed_listeners.remove(listener)

    def _validate_property_change(self, property_name: str, old_value : Any, new_value : Any) -> bool:
        for listener in self._changing_listeners:
            if not listener.on_property_changing(self, property_name, old_value, new_value):
                return False
        return True

    def _notify_property_changed(self, property_name: str) -> None:
        for listener in self._changed_listeners:
            listener.on_property_changed(self, property_name)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if self._name != value:
            if self._validate_property_change("name", self._name, value):
                self._name = value
                self._notify_property_changed("name")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if self._email != value:
            if self._validate_property_change("email", self._email, value):
                self._email = value
                self._notify_property_changed("email")


class EmailValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj : DataChangingProtocol, property_name: str, old_value: Any, new_value : Any) -> bool:
        if property_name != 'email':
            return True
        if not isinstance(new_value,str):
            print("[EmailValidator] Ошибка: Email должно быть строкой!")
            return False
        if len(new_value) <= 5:
            print("[EmailValidator] Ошибка: Email слишком короткий!")
            return False
        if new_value.count('@') != 1 or not '.' in new_value.split('@')[-1] or '.' in new_value.split('@')[0]:
            print("[EmailValidator] Ошибка: Email не корректен!")
            return False
        return True


class NameValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj  : DataChangingProtocol, property_name: str, old_value : Any, new_value : Any) -> bool:
        if property_name != "name":
            return True
        if not isinstance(new_value,str):
            print("[NameValidator] Ошибка: имя должно быть строкой!")
            return False
        if len(new_value) == 0:
            print("[NameValidator] Ошибка: имя не может быть пустым!")
            return False
        if not new_value.isalpha():
            print("[NameValidator] Ошибка: имя не должно содержать цифр!")
            return False
        return True


class ConsoleLogger(PropertyChangedListenerProtocol):
    def on_property_changed(self, obj : DataChangedProtocol, property_name: str) -> None:
        print(f"[ConsoleLogger] Свойство '{property_name}' изменено. Новое значение: {getattr(obj, property_name)}")


def main():
    user = User()
    user.add_property_changing_listener(EmailValidator())
    user.add_property_changing_listener(NameValidator())
    user.add_property_changed_listener(ConsoleLogger())

    print("\nКорректный ввод")
    user.name = "Name"
    user.email = "NameDigits@example.com"

    print("\nНекорректный ввод")
    user.name = ""
    user.email = "AA@AAAA@AAAA.ru"

    print("\nИтоговые значения:")
    print(f"Имя: {user.name}, Email: {user.email}")

if __name__ == "__main__":
    main()