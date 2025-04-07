class Point2d:
    _WIDTH = 100
    _HEIGHT = 100
    _x : int
    _y : int

    def __init__(self,x : int,y : int):
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @x.setter
    def x(self, value: int):
        if 0 <= value <= self._WIDTH:
            self._x = value
        else:
            raise ValueError(f"y must be between 0 and {self._WIDTH}")

    @y.setter
    def y(self, value: int):
        if 0 <= value <= self._HEIGHT:
            self._y = value
        else:
            raise ValueError(f"y must be between 0 and {self._WIDTH}")

    def __eq__(self,other):
        if not isinstance(other, Point2d):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return f"P2d({self.x},{self.y})"

    def __repr__(self):
        return str(self)

class Vector2d:
    _x : int
    _y : int

    def __init__(self, x: int, y:int):
        self.x = x
        self.y = y

    @classmethod
    def from_points(cls, start: Point2d, end: Point2d):
        return cls(end.x - start.x, end.y - start.y)

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @x.setter
    def x(self, value: int):
        self._x = value

    @y.setter
    def y(self, value: int):
        self._y = value

    def __getitem__(self, item : int):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        raise IndexError("Vector2d index out of range")

    def __setitem__(self, key : int, value : int):
        if key == 0:
            self.x = value
            return
        if key == 1:
            self.y = value
            return
        raise IndexError("Vector2d index out of range")

    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self):
        return 2

    def __eq__(self, other):
        if isinstance(other, Vector2d):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return f"V2d({self.x},{self.y})"

    def __repr__(self):
        return str(self)

    def __abs__(self):
        return (self.x*self.x + self.y*self.y)**0.5

    def __add__(self, other):
        if isinstance(other,Vector2d):
            return Vector2d(self.x+other.x,self.y+other.y)
        raise TypeError(f"can only add Vector2d(not{type(other)}) to Vector2d")

    def __sub__(self, other):
        if isinstance(other,Vector2d):
            return Vector2d(self.x-other.x,self.y-other.y)
        raise TypeError(f"can only sub Vector2d(not{type(other)}) to Vector2d")

    def __mul__(self, value : int):
        if isinstance(value,int):
            return Vector2d(self.x * value,self.y * value)
        raise TypeError("Can only multiply Vector2d by int")

    def __floordiv__(self, value : int):
        if isinstance(value,int):
            return Vector2d(self.x // value,self.y // value)
        raise TypeError("Can only divide Vector2d by int")

    def dot_product(self,other) -> int:
        if isinstance(other,Vector2d):
            return self.x * other.x  + self.y * other.y
        raise TypeError("Can only dot product Vector2d by Vector2d")

    @staticmethod
    def dot_product_static(v1,v2) -> int:
        if isinstance(v1,Vector2d) and isinstance(v2,Vector2d):
            return v1.x * v2.x + v1.y * v2.y
        raise TypeError("Can only dot product Vector2d by Vector2d")

    def vector_product(self,other) -> int:
        if isinstance(other,Vector2d):
            return self.x * other.y - self.y * other.x
        raise TypeError("Can only vector product Vector2d by Vector2d")

    @staticmethod
    def vector_product_static(v1,v2) -> int:
        if isinstance(v1,Vector2d) and isinstance(v2,Vector2d):
            return v1.x * v2.y - v1.y * v2.x
        raise TypeError("Can only vector product Vector2d by Vector2d")

    @staticmethod
    def triple_product(v1, v2, v3) -> float:
        """Смешанное произведение трех векторов (в 2D это скалярное произведение v1 × v2 и v3)"""
        tmp = Vector2d.vector_product_static(v1, v2)
        return tmp * v3.x + tmp * v3.y

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

    print(c.vector_product(d), Vector2d.vector_product_static(c, d))

    print(Vector2d.triple_product(c,d,e))

if __name__ == "__main__":
    main()
