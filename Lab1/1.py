from typing import Self, Generator
WIDTH = 100
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

    @property
    def y(self) -> int:
        return self._y

    @x.setter
    def x(self, value: int) -> None:
        if 0 <= value <= WIDTH:
            self._x = value
        else:
            raise ValueError(f"y must be between 0 and {WIDTH}")

    @y.setter
    def y(self, value: int) -> None:
        if 0 <= value <= HEIGHT:
            self._y = value
        else:
            raise ValueError(f"y must be between 0 and {WIDTH}")

    def __eq__(self,other : Self)-> bool:
        if not isinstance(other, Point2d):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other : Self)-> bool:
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
    def from_points(cls, start: Point2d, end: Point2d) -> Self:
        return cls(end.x - start.x, end.y - start.y)

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

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

    def __eq__(self, other : Self) -> bool:
        if isinstance(other, Vector2d):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other : Self) -> bool:
        return not(self == other)

    def __str__(self) -> str:
        return f"V2d({self.x},{self.y})"

    def __repr__(self) -> str:
        return str(self)

    def __abs__(self) -> float:
        return (self.x*self.x + self.y*self.y)**0.5

    def __add__(self, other : Self) -> Self:
        if isinstance(other,Vector2d):
            return Vector2d(self.x+other.x,self.y+other.y)
        raise TypeError(f"can only add Vector2d(not{type(other)}) to Vector2d")

    def __sub__(self, other : Self) -> Self:
        if isinstance(other,Vector2d):
            return Vector2d(self.x-other.x,self.y-other.y)
        raise TypeError(f"can only sub Vector2d(not{type(other)}) to Vector2d")

    def __mul__(self, value : int) -> Self:
        if isinstance(value,int):
            return Vector2d(self.x * value,self.y * value)
        raise TypeError("Can only multiply Vector2d by int")

    def __rmul__(self, value : int) -> Self:
        if isinstance(value,int):
            return Vector2d(self.x * value,self.y * value)
        raise TypeError("Can only multiply Vector2d by int")

    def __floordiv__(self, value : int) -> Self:
        if isinstance(value,int):
            return Vector2d(self.x // value,self.y // value)
        raise TypeError("Can only divide Vector2d by int")

    def dot_product(self,other : Self) -> int:
        if isinstance(other,Vector2d):
            return self.x * other.x  + self.y * other.y
        raise TypeError("Can only dot product Vector2d by Vector2d")

    @staticmethod
    def dot_product_static(v1 : Self, v2 : Self) -> int:
        if isinstance(v1,Vector2d) and isinstance(v2,Vector2d):
            return v1.x * v2.x + v1.y * v2.y
        raise TypeError("Can only dot product Vector2d by Vector2d")

    def cross_product(self,other : Self) -> Self:
        if isinstance(other,Vector2d):
            return Vector2d(self.x * other.y - self.y * other.x,0)
        raise TypeError("Can only vector product Vector2d by Vector2d")

    @staticmethod
    def cross_product_static(v1 : Self,v2 : Self) -> Self:
        if isinstance(v1,Vector2d) and isinstance(v2,Vector2d):
            return Vector2d(v1.x * v2.y - v1.y * v2.x,0)
        raise TypeError("Can only vector product Vector2d by Vector2d")

    def triple_product(self, v2 : Self, v3 : Self) -> int:
        if isinstance(v2,Vector2d) and isinstance(v3,Vector2d):
            return self.dot_product(Vector2d.cross_product(v2,v3))
        else:
            raise TypeError("Can only triple product Vector2d by Vector2d by Vector2d")

    @staticmethod
    def triple_product_static(v1 : Self, v2 : Self, v3 : Self) -> int:
        if isinstance(v1,Vector2d) and isinstance(v2,Vector2d) and isinstance(v3,Vector2d):
            return v1.dot_product(Vector2d.cross_product(v2,v3))
        else:
            raise TypeError("Can only triple product Vector2d by Vector2d by Vector2d")

def main():
    a = Point2d(5,5)
    b = Point2d(4, 1)
    print(a,b)

    c = Vector2d(5,3)
    d = Vector2d.from_points(b,a)

    print(c,d)

    c[0] = 4
    d[0] = c[0]

    print(c,d)

    print(len(c))

    print(c == d, c == a, c == c)
    print(c != d, c != a, c != c)

    for i in c:
        print(i)

    e = c + d
    print(c + d,e)
    #c + a
    print(c-d)

    print(abs(c))

    print(c*5)
    print(c//2)

    print(c.dot_product(d), Vector2d.dot_product_static(c,d))

    print(c.cross_product(d), Vector2d.cross_product_static(c, d))

    print(Vector2d.triple_product(c,d,e))

if __name__ == "__main__":
    main()
