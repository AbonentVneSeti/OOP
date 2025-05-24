from abc import ABC, abstractmethod
from typing import List

# Протокол для слушателя изменений свойства
class PropertyChangedListenerProtocol(ABC):
    @abstractmethod
    def on_property_changed(self, obj, property_name: str) -> None:
        pass

# Протокол для добавления/удаления слушателей изменений
class DataChangedProtocol(ABC):
    @abstractmethod
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        pass

    @abstractmethod
    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        pass

# Протокол для слушателя валидации изменений свойства
class PropertyChangingListenerProtocol(ABC):
    @abstractmethod
    def on_property_changing(self, obj, property_name: str, old_value, new_value) -> bool:
        pass

# Протокол для добавления/удаления валидаторов
class DataChangingProtocol(ABC):
    @abstractmethod
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        pass

    @abstractmethod
    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        pass

class Person(DataChangingProtocol, DataChangedProtocol):
    def __init__(self):
        self._changing_listeners: List[PropertyChangingListenerProtocol] = []
        self._changed_listeners: List[PropertyChangedListenerProtocol] = []
        self._name = ""
        self._age = 0

    # DataChangingProtocol методы
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        self._changing_listeners.append(listener)

    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        self._changing_listeners.remove(listener)

    # DataChangedProtocol методы
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        self._changed_listeners.append(listener)

    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        self._changed_listeners.remove(listener)

    # Валидация изменений
    def _validate_property_change(self, property_name: str, old_value, new_value) -> bool:
        for listener in self._changing_listeners:
            if not listener.on_property_changing(self, property_name, old_value, new_value):
                return False
        return True

    # Уведомление об изменениях
    def _notify_property_changed(self, property_name: str) -> None:
        for listener in self._changed_listeners:
            listener.on_property_changed(self, property_name)

    # Свойства с валидацией и уведомлениями
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if self._name != value:
            if self._validate_property_change("name", self._name, value):
                old_value = self._name
                self._name = value
                self._notify_property_changed("name")

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if self._age != value:
            if self._validate_property_change("age", self._age, value):
                old_value = self._age
                self._age = value
                self._notify_property_changed("age")

# Валидатор: возраст не может быть отрицательным
class AgeValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj, property_name: str, old_value, new_value) -> bool:
        if property_name == "age" and new_value < 0:
            print("[AgeValidator] Ошибка: возраст не может быть отрицательным!")
            return False
        return True

# Валидатор: имя не может быть пустым
class NameValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj, property_name: str, old_value, new_value) -> bool:
        if property_name == "name" and len(new_value.strip()) == 0:
            print("[NameValidator] Ошибка: имя не может быть пустым!")
            return False
        return True

# Логгер изменений
class ChangeLogger(PropertyChangedListenerProtocol):
    def on_property_changed(self, obj, property_name: str) -> None:
        print(f"[ChangeLogger] Свойство '{property_name}' изменено. Новое значение: {getattr(obj, property_name)}")

# Еще один логгер
class AnotherLogger(PropertyChangedListenerProtocol):
    def on_property_changed(self, obj, property_name: str) -> None:
        print(f"[AnotherLogger] {property_name} = {getattr(obj, property_name)}")

# Создаем объект и слушатели
person = Person()
person.add_property_changing_listener(AgeValidator())
person.add_property_changing_listener(NameValidator())
person.add_property_changed_listener(ChangeLogger())
person.add_property_changed_listener(AnotherLogger())

# Успешные изменения
person.name = "Алиса"  # Изменится и вызовет логгеры
person.age = 25        # Изменится и вызовет логгеры

# Некорректные изменения (блокируются валидаторами)
person.name = ""       # Блокируется NameValidator
person.age = -5        # Блокируется AgeValidator

# Проверка значений
print("\nИтоговые значения:")
print(f"Имя: {person.name}, Возраст: {person.age}")