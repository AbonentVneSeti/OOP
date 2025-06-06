from typing import Self

class KeyboardStateSaver:
    def __init__(self, state: dict) -> None:
        self.state = state
        
    @classmethod
    def from_keyboard(cls, keyboard) -> Self:
        key_bindings = {}
        for bind, command in keyboard.key_bindings.items():
            if command is None:
                key_bindings[bind] = [None, None]
            else:
                cmd_data = command.__dict__.copy()
                cmd_data.pop("keyboard")
                key_bindings[bind] = [command.__class__.__name__, cmd_data]

        return cls({
            "key_bindings": key_bindings,
            "output_state": keyboard.output
        })