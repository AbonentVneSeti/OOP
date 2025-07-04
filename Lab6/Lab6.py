from v_keyboard import VirtualKeyboard
from commands import PrintCharCommand


def main():
    keyboard = VirtualKeyboard()

    if not keyboard.load_state():
        print("No saved state found, using defaults")
    else:
        print("Keyboard state loaded:",PrintCharCommand.text)

    with open("data/keyboard_log.txt", "w") as log_file:
        def print_and_log(message) -> None:
            print(message)
            log_file.write(message + "\n")

        print_and_log(keyboard.press_key("a"))
        print_and_log(keyboard.press_key("b"))
        print_and_log(keyboard.press_key("c"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("redo"))
        print_and_log(keyboard.press_key("ctrl++"))
        print_and_log(keyboard.press_key("ctrl+-"))
        print_and_log(keyboard.press_key("ctrl+p"))
        print_and_log(keyboard.press_key("d"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("undo"))

        keyboard.save_state()
        print_and_log("Keyboard state saved")

if __name__ == "__main__":
    main()