from typing import Protocol, Sequence, TypeVar, Optional
from serializers import ISerializer
T = TypeVar('T')


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
    def __init__(self, filename: str, serializer : ISerializer) -> None:
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
        return next((item_ for item_ in self.get_all() if item_.id == id), None)

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
            raise ValueError("Item not found")

    def delete(self, item: T) -> None:
        data = self._load_data()
        data = [item_ for item_ in data if item_.id != item.id]
        self._save_data(data)