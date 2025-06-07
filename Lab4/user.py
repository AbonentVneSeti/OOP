from typing import List, Any
from protocols import DataChangingProtocol, PropertyChangingListenerProtocol, DataChangedProtocol, PropertyChangedListenerProtocol


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