from enum import Enum
from typing import Self

class Color(Enum):
    TRANSPARENT = 0
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    DEFAULT = 39
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96

class Printer:
    _font: dict[str, list[str]] = {}
    _size: tuple[int, int] = ()

    @staticmethod
    def init() -> None:
        for _ in range(14):
            print()
        Printer.load_font(filename="font.txt")

    def __init__(self, color: Color, position: tuple[int, int], symbol: str, background_color: Color = Color.TRANSPARENT) -> None:
        self.color = color
        self.background_color = background_color
        self.symbol = symbol
        self.initial_x, self.initial_y = position
        self.current_x, self.current_y = position

    @classmethod
    def load_font(cls, filename: str) -> None:
        with open(file=filename) as f:
            font_file = f.readlines()

        size_parts = font_file[0][:-1].split(sep='x')
        if len(size_parts) != 2:
            raise ValueError(f"Некорректный формат размера в файле: {size_parts}")

        cls._size = (int(size_parts[0]), int(size_parts[1]))

        if (len(font_file) - 1) % (cls._size[1] + 1) != 0:
            raise ValueError(f"Некорректный размер файла")

        for char in range(1, len(font_file), cls._size[0] + 1):
            cls._font[font_file[char][:-1]] = [font_file[i][:-1] for i in range(char + 1, char + cls._size[0] + 1)]

    @classmethod
    def print_(cls, text: str, color: Color = Color.DEFAULT, position: tuple[int, int] = (0,0), symbol: str = '*', background_color: Color = Color.TRANSPARENT) -> None:
        if not cls._font or not cls._size:
            raise ValueError("Шрифт не загружен. Сначала вызовите Printer.load_font()")

        x, y = position
        for char in text:
            if char not in cls._font:
                raise ValueError(f"Символ {char} отсутствует в шрифте.")

            for line_num, line in enumerate(cls._font[char]):
                rendered = line.replace("*", symbol)
                print(f"\033[{y + line_num + 1};{x + 1}H{f"\033[{color.value}m\033[{background_color.value + 10}m{rendered}"}", end="")

            x += cls._size[0]
        print()

    def __enter__(self) -> Self:
        print(f"\033[{self.color.value}m\033[{self.background_color.value + 10}m{''}", end="")
        return self

    def __exit__(self, *args) -> None:
        print(f"\033[{Color.TRANSPARENT.value}m\033[{Color.TRANSPARENT.value + 10}m{''}", end="")

    def print(self, text: str) -> None:
        if not self._font or not self._size:
            raise ValueError("Шрифт не загружен. Сначала вызовите Printer.load_font()")

        x, y = self.current_x, self.current_y
        for char in text:
            if char not in self._font:
                continue

            for line_num, line in enumerate(self._font[char]):
                rendered = line.replace("*", self.symbol)
                print(f"\033[{y + line_num + 1};{x + 1}H{rendered}", end="")

            x += self._size[1]
        self.current_x = x


if __name__ == "__main__":
    Printer.init()

    Printer.print_("AB", Color.RED, (0, 0), "#", background_color=Color.TRANSPARENT)
    Printer.print_("AB")
    with Printer(Color.BLACK, (5, 5), "A", background_color=Color.WHITE) as printer:
        printer.print("DDDD")
        printer.background_color = Color.RED
        printer.print(" AB")
