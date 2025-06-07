from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...

    @abstractmethod
    def undo(self) -> None:
        ...

    @abstractmethod
    def redo(self) -> None:
        ...


class PrintCharCommand(Command):
    text = ""

    def __init__(self, char: str) -> None:
        self.char = char

    def execute(self) -> str:
        PrintCharCommand.text += self.char
        return PrintCharCommand.text

    def undo(self) -> str:
        PrintCharCommand.text = PrintCharCommand.text[:-1]
        return PrintCharCommand.text

    def redo(self) -> str:
        return self.execute()


class VolumeUpCommand(Command):
    def __init__(self, amount: int = 20) -> None:
        self.amount = amount

    def execute(self) -> str:
        return f"volume increased by {self.amount}%"

    def undo(self) -> str:
        return f"volume decreased by {self.amount}%"

    def redo(self) -> str:
        return self.execute()


class VolumeDownCommand(Command):
    def __init__(self, amount: int = 20) -> None:
        self.amount = amount

    def execute(self) -> str:
        return f"volume decreased by {self.amount}%"

    def undo(self) -> str:
        return f"volume increased by {self.amount}%"

    def redo(self) -> str:
        return self.execute()


class MediaPlayerCommand(Command):
    def __init__(self, is_playing: bool = False) -> None:
        self.is_playing = is_playing

    def execute(self) -> str:
        if self.is_playing:
            self.is_playing = False
            return "media player closed"
        else:
            self.is_playing = True
            return "media player launched"

    def undo(self) -> str:
        return self.execute()


    def redo(self) -> str:
        return self.execute()