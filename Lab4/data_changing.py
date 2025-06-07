from protocols import PropertyChangingListenerProtocol, DataChangingProtocol
from typing import Any


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