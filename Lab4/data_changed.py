from protocols import DataChangedProtocol, PropertyChangedListenerProtocol


class ConsoleLogger(PropertyChangedListenerProtocol):
    def on_property_changed(self, obj : DataChangedProtocol, property_name: str) -> None:
        print(f"[ConsoleLogger] Свойство '{property_name}' изменено. Новое значение: {getattr(obj, property_name)}")