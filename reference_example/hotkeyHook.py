import keyboard


def on_triggered():
    main.text_to_print = "a" + main.text_to_print
    print(main.text_to_print)


def main():
    main.text_to_print = 'default_predefined_text'
    shortcut = 'alt+x'
    print('Hotkey set as:', shortcut)
    keyboard.add_hotkey(shortcut, on_triggered)
    print("Press ESC to stop.")
    keyboard.wait('esc')


if __name__ == '__main__':
    main()
