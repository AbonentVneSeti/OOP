import datetime, re
from typing import List, Protocol


class LogFilterProtocol(Protocol):
    def match(self, text: str) -> bool:
        pass


class LogHandlerProtocol(Protocol):
    def handle(self, text: str) -> None:
        pass


class SimpleLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def match(self, text: str) -> bool:
        return self.pattern in text


class ReLogFilter(LogFilterProtocol):
    def __init__(self, regex_pattern: str) -> None:
        self.regex = re.compile(regex_pattern)

    def match(self, text: str) -> bool:
        return bool(self.regex.search(text))


class ConsoleHandler(LogHandlerProtocol):
    def handle(self, text: str) -> None:
        print(f"[CONSOLE] {text}")


class FileHandler(LogHandlerProtocol):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def handle(self, text: str) -> None:
        with open(self.file_path, 'a', encoding='utf-8') as file:
            file.write(f"{text}\n")


class SocketHandler(LogHandlerProtocol):
    def handle(self, text: str) -> None:
        print(f"[SOCKET] Sending message: {text}")


class SyslogHandler(LogHandlerProtocol):
    def handle(self, text: str) -> None:
        print(f"[SYSLOG] Logging to system log: {text}")


class Logger:
    def __init__(self,
                 filters: List[LogFilterProtocol] = None,
                 handlers: List[LogHandlerProtocol] = None) -> None:
        self.filters = filters if filters is not None else []
        self.handlers = handlers if handlers is not None else []

    def log(self, text: str) -> None:
        for log_filter in self.filters:
            if not log_filter.match(text):
                return
        text =f"[{datetime.datetime.now()}]: {text}"

        for handler in self.handlers:
            handler.handle(text)


def main():
    error_filter = SimpleLogFilter("ERROR")
    number_filter = ReLogFilter(r'\d{3}')

    console_handler = ConsoleHandler()
    file_handler = FileHandler("log.log")
    syslog_handler = SyslogHandler()

    logger = Logger(
        filters=[error_filter, number_filter],
        handlers=[console_handler, file_handler, syslog_handler]
    )

    messages = [
        "INFO: test0",
        "ERROR: test1",
        "WARNING: test2",
        "DEBUG: test3",
        "ERROR: test100"
    ]

    print("Демонстрация работы системы логирования:")
    for msg in messages:
        print(f"Попытка логирования: '{msg}'")
        logger.log(msg)

if __name__ == "__main__":
    main()