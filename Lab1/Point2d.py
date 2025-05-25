WIDTH = 100
HEIGHT = 100

class Point2d:
    _x : int
    _y : int

    def __init__(self, x : int, y : int) -> None:
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
            raise ValueError(f"x must be between 0 and {WIDTH}")

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
        return self.x == other.x and self.y == other.y

    def __ne__(self, other : 'Point2d')-> bool:
        return not (self == other)

    def __str__(self) -> str:
        return f"P2d({self.x},{self.y})"

    def __repr__(self) -> str:
        return f"Point2d(x = {self.x}, y = {self.y})"