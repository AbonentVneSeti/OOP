from keyboard import Keyboard

if __name__ == "__main__":
    keyboard = Keyboard()

    if not keyboard.load_state():
        print("No saved state found, using defaults")
    else:
        print("Keyboard state loaded")
        print(keyboard.output)

    with open("data/keyboard_log.txt", "w") as log_file:
        def print_and_log(message) -> None:
            print(message)
            log_file.write(message + "\n")

        print_and_log(keyboard.press_key("a"))
        print_and_log(keyboard.press_key("a"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("ctrl++"))
        print_and_log(keyboard.press_key("ctrl++"))
        print_and_log(keyboard.press_key("ctrl++"))
        print_and_log(keyboard.press_key("ctrl++"))
        print_and_log(keyboard.press_key("ctrl++"))
        print_and_log(keyboard.press_key("ctrl+-"))
        print_and_log(keyboard.press_key("ctrl+p"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("redo"))
        print_and_log(keyboard.press_key("undo"))


        keyboard.save_state()
        print_and_log("Keyboard state saved")