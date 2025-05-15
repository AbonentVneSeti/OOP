import random
from typing import Generator
WIDTH = 150
HEIGHT = 100

class Point2d:
    _x : int
    _y : int

    def __init__(self,x : int,y : int) -> None:
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        if 0 <= value <= WIDTH:
            self._x = value
        else:
            raise ValueError(f"y must be between 0 and {WIDTH}")

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        if 0 <= value <= HEIGHT:
            self._y = value
        else:
            raise ValueError(f"y must be between 0 and {HEIGHT}")

    def __eq__(self,other : 'Point2d')-> bool:
        if not isinstance(other, Point2d):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other : 'Point2d')-> bool:
        return not (self == other)

    def __str__(self) -> str:
        return f"P2d({self.x},{self.y})"

    def __repr__(self) -> str:
        return str(self)

class Vector2d:
    _x : int
    _y : int

    def __init__(self, x: int, y:int) -> None:
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
        if isinstance(other, Vector2d):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other : 'Vector2d') -> bool:
        return not(self == other)

    def __str__(self) -> str:
        return f"V2d({self.x},{self.y})"

    def __repr__(self) -> str:
        return str(self)

    def __abs__(self) -> float:
        return (self.x*self.x + self.y*self.y)**0.5

    def __add__(self, other : 'Vector2d') -> 'Vector2d':
        if isinstance(other,Vector2d):
            return Vector2d(self.x+other.x,self.y+other.y)
        raise TypeError(f"can only add Vector2d(not{type(other)}) to Vector2d")

    def __sub__(self, other : 'Vector2d') -> 'Vector2d':
        if isinstance(other,Vector2d):
            return Vector2d(self.x-other.x,self.y-other.y)
        raise TypeError(f"can only sub Vector2d(not{type(other)}) to Vector2d")

    def __mul__(self, value : int) -> 'Vector2d':
        if isinstance(value,int):
            return Vector2d(self.x * value,self.y * value)
        raise TypeError("Can only multiply Vector2d by int")

    def __rmul__(self, value : int) -> 'Vector2d':
        if isinstance(value,int):
            return Vector2d(self.x * value,self.y * value)
        raise TypeError("Can only multiply Vector2d by int")

    def __floordiv__(self, value : int) -> 'Vector2d':
        if isinstance(value,int):
            return Vector2d(self.x // value,self.y // value)
        raise TypeError("Can only divide Vector2d by int")

    @staticmethod
    def dot_product_static(v1: 'Vector2d', v2: 'Vector2d') -> int:
        if isinstance(v1, Vector2d) and isinstance(v2, Vector2d):
            return v1.x * v2.x + v1.y * v2.y
        raise TypeError("Can only dot product Vector2d by Vector2d")

    def dot_product(self,other : 'Vector2d') -> int:
        if isinstance(other,Vector2d):
            return self.x * other.x  + self.y * other.y
        raise TypeError("Can only dot product Vector2d by Vector2d")

    @staticmethod
    def cross_product_static(v1: 'Vector2d', v2: 'Vector2d') -> 'Vector2d':
        if isinstance(v1, Vector2d) and isinstance(v2, Vector2d):
            return Vector2d(v1.x * v2.y - v1.y * v2.x, 0)
        raise TypeError("Can only vector product Vector2d by Vector2d")

    def cross_product(self, other: 'Vector2d') -> 'Vector2d':
        if isinstance(other, Vector2d):
            return Vector2d(self.x * other.y - self.y * other.x, 0)
        raise TypeError("Can only vector product Vector2d by Vector2d")

    @staticmethod
    def triple_product_static(v1 : 'Vector2d', v2 : 'Vector2d', v3 : 'Vector2d') -> int:
        if isinstance(v1,Vector2d) and isinstance(v2,Vector2d) and isinstance(v3,Vector2d):
            return v1.dot_product(Vector2d.cross_product(v2,v3))
        else:
            raise TypeError("Can only triple product Vector2d by Vector2d by Vector2d")

    def triple_product(self, v2 : 'Vector2d', v3 : 'Vector2d') -> int:
        if isinstance(v2,Vector2d) and isinstance(v3,Vector2d):
            return self.dot_product(Vector2d.cross_product(v2,v3))
        else:
            raise TypeError("Can only triple product Vector2d by Vector2d by Vector2d")

def main():
    print("Класс Point2d:")
    x = random.randint(0,WIDTH)
    y = random.randint(0,HEIGHT)

    a = Point2d(x,y)
    print(f"Point2d по x={x}, y={y}: {a}")
    print()

    x = random.randint(0,WIDTH)
    y = random.randint(0,HEIGHT)

    b = Point2d(x,y)

    print(f"{a} == {a}: {a == a}")
    print(f"{a} == {b}: {a == b}")
    print()

    print("Класс Vector2d:")
    vec1 = Vector2d(x,y)
    print(f"Vector2d по x={x}, y={y}: vec1={vec1}")
    vec2 = Vector2d.from_points(a,b)
    print(f"Vector2d по start={a}, end={b}: vec2={vec2}")
    print()

    print("Доступ по индексу:")
    for i in range(len(vec1)): print(f"vec1[{i}] = {vec1[i]}")
    print()

    print(f"Итерирование {vec1}:")
    for i in vec1: print(i)
    print()

    print(f"{vec1} == {vec2}: {vec1 == vec2}")
    print(f"{vec1} == {vec1}: {vec1 == vec1}")
    print()

    print(f"abs({vec1}) = {abs(vec1)}")
    print(f"{vec1} + {vec2} = {vec1 + vec2}")
    print(f"{vec1} - {vec2} = {vec1 - vec2}")
    randval = random.randint(0,15)
    print(f"{vec1}*{randval} = {vec1 * randval}")
    print(f"{randval}*{vec1} = {randval * vec1}")
    randval = random.randint(1, 15)
    print(f"{vec1}//{randval} = {vec1 // randval}")
    print()

    print(f"Скалярное произведение {vec1}.dot_product({vec2}) = {vec1.dot_product(vec2)}")
    print(f"Статическое скалярное произведение Vector2d.dot_product_static({vec1},{vec2}) = {Vector2d.dot_product_static(vec1,vec2)}")
    print()

    print(f"Векторное произведение {vec1}.cross_product({vec2}) = {vec1.cross_product(vec2)}")
    print(f"Статическое векторное произведение Vector2d.cross_product_static({vec1},{vec2}) = {Vector2d.cross_product_static(vec1, vec2)}")
    print()

    vec3 = vec1+vec2
    print(f"Смешанное произведение {vec1}.triple_product({vec2},{vec3}) = {vec1.triple_product(vec2,vec3)}")
    print(f"Статическое смешанное произведение Vector2d.triple_product_static({vec1},{vec2},{vec3}) = {Vector2d.triple_product_static(vec1, vec2, vec3)}")

if __name__ == "__main__":
    main()
