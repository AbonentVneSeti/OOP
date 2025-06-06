from dataclasses import dataclass, field
from typing import Optional, Self


@dataclass
class User:
    id: int
    login: str
    password: str = field(repr=False, compare=False)
    name: str = field(compare=False)
    email: Optional[str] = field(default=None, compare=False)
    address: Optional[str] = field(default=None, compare=False)

    def __lt__(self, other: Self) -> bool:
        return self.name.lower() < other.name.lower()