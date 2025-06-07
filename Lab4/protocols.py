from typing import Any, Protocol


class PropertyChangingListenerProtocol(Protocol):
    def on_property_changing(self, obj : Any, property_name: str, old_value : Any, new_value : Any) -> bool:
        pass


class DataChangingProtocol(Protocol):
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        pass

    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        pass


class PropertyChangedListenerProtocol(Protocol):
    def on_property_changed(self, obj : Any, property_name: str) -> None:
        pass


class DataChangedProtocol(Protocol):
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        pass

    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        pass