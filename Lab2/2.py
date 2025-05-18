from enum import Enum
from typing import Self, Optional


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
    _size: tuple[int, int] = (0, 0)

    @staticmethod
    def init() -> None:
        print("\033[2J", end="")

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
    def _get_escape_code(cls, color: Color, background: bool = False) -> str:
        if color == Color.TRANSPARENT:
            return ""
        code = color.value + (10 if background else 0)
        return f"\033[{code}m"

    @classmethod
    def print_(
            cls,
            text: str,
            color: Color = Color.DEFAULT,
            position: tuple[int, int] = (0, 0),
            symbol: str = '*',
            background_color: Color = Color.TRANSPARENT
    ) -> None:
        if not cls._font:
            raise ValueError("Шрифт не загружен. Сначала вызовите Printer.load_font()")

        x, y = position
        fg_code = cls._get_escape_code(color)
        bg_code = cls._get_escape_code(background_color, background=True)
        reset_code = "\033[0m"

        for char in text:
            if char not in cls._font:
                raise ValueError(f"Символ {char} отсутствует в шрифте.")

            char_lines = cls._font[char]
            for dy, line in enumerate(char_lines):
                rendered = line.replace('*', symbol)
                print(
                    f"\033[{y + dy + 1};{x + 1}H"
                    f"{fg_code}{bg_code}{rendered}{reset_code}",
                    end=""
                )

            x += cls._size[0]

        print(flush=True)

    def __init__(
            self,
            color: Color,
            position: tuple[int, int],
            symbol: str = '*',
            background_color: Color = Color.TRANSPARENT
    ) -> None:
        self.color = color
        self.background_color = background_color
        self.symbol = symbol
        self.initial_x, self.initial_y = position
        self.current_x, self.current_y = position

    def __enter__(self) -> Self:
        fg_code = self._get_escape_code(self.color)
        bg_code = self._get_escape_code(self.background_color, background=True)
        print(f"{fg_code}{bg_code}", end="")
        return self

    def __exit__(self, *args) -> None:
        print("\033[0m", end="", flush=True)

    def print(self, text: str) -> None:
        if not self._font:
            raise ValueError("Шрифт не загружен. Сначала вызовите Printer.load_font()")

        x, y = self.current_x, self.current_y
        for char in text:
            if char not in self._font:
                continue

            char_lines = self._font[char]
            for dy, line in enumerate(char_lines):
                rendered = line.replace('*', self.symbol)
                print(f"\033[{y + dy + 1};{x + 1}H{rendered}", end="")

            x += self._size[0]

        self.current_x = x
        print(flush=True)

if __name__ == "__main__":
    Printer.init()
    Printer.load_font('font.txt')

    Printer.print_("ABCD", Color.RED, (0, 0), "#", background_color=Color.TRANSPARENT)
    with Printer(Color.BLACK, (5, 5), "A", background_color=Color.WHITE) as printer:
        printer.print("DDDD")
        printer.print(" AB")