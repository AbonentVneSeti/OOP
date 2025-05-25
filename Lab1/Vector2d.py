from typing import Generator
from Point2d import Point2d

class Vector2d:
    _x : int
    _y : int

    def __init__(self, x : int, y : int) -> None:
        self.x = x
        self.y = y

    @classmethod
    def from_points(cls, start: Point2d, end: Point2d) -> 'Vector2d':
        return cls(end.x - start.x, end.y - start.y)

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    def __getitem__(self, index : int) -> int:
        match index:
            case 0:
                return self.x
            case 1:
                return self.y
            case _:
                raise IndexError("Vector2d: index out of range")

    def __setitem__(self, index : int, value : int) -> None:
        match index:
            case 0:
                self.x = value
            case 1:
                self.y = value
            case _:
                raise IndexError("Vector2d: index out of range")

    def __iter__(self) -> Generator:
        yield self.x
        yield self.y

    def __len__(self) -> int:
        return 2

    def __eq__(self, other : 'Vector2d') -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other : 'Vector2d') -> bool:
        return not(self == other)

    def __str__(self) -> str:
        return f"V2d({self.x},{self.y})"

    def __repr__(self) -> str:
        return f"Vector2d(x = {self.x}, y = {self.y})"

    def __abs__(self) -> float:
        return (self.x*self.x + self.y*self.y)**0.5

    def __add__(self, other : 'Vector2d') -> 'Vector2d':
        return Vector2d(self.x+other.x,self.y+other.y)

    def __sub__(self, other : 'Vector2d') -> 'Vector2d':
        return Vector2d(self.x-other.x,self.y-other.y)

    def __mul__(self, value : int) -> 'Vector2d':
        return Vector2d(self.x * value,self.y * value)

    def __rmul__(self, value : int) -> 'Vector2d':
        return Vector2d(self.x * value,self.y * value)

    def __floordiv__(self, value : int) -> 'Vector2d':
        return Vector2d(self.x // value,self.y // value)

    @staticmethod
    def dot_product_static(v1: 'Vector2d', v2: 'Vector2d') -> int:
        return v1.x * v2.x + v1.y * v2.y

    def dot_product(self,other : 'Vector2d') -> int:
        return self.x * other.x  + self.y * other.y

    @staticmethod
    def cross_product_static(v1: 'Vector2d', v2: 'Vector2d') -> 'Vector2d':
        return Vector2d(v1.x * v2.y - v1.y * v2.x, 0)

    def cross_product(self, other: 'Vector2d') -> 'Vector2d':
        return Vector2d(self.x * other.y - self.y * other.x, 0)

    @staticmethod
    def triple_product_static(v1 : 'Vector2d', v2 : 'Vector2d', v3 : 'Vector2d') -> int:
        return v1.dot_product(Vector2d.cross_product(v2,v3))

    def triple_product(self, v2 : 'Vector2d', v3 : 'Vector2d') -> int:
        return self.dot_product(Vector2d.cross_product_static(v2,v3))
