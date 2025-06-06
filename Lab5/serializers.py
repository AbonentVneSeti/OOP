from typing import Protocol
import json
from dataclasses import asdict, is_dataclass
from user import User

class ISerializer(Protocol):
    @staticmethod
    def serialize(data: list) -> bytes:
        pass

    @staticmethod
    def deserialize(data_bytes: bytes) -> list:
        pass


class JSONSerializer(ISerializer):
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