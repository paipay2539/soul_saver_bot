import keyboard

text_to_print = 'default_predefined_text'
shortcut = 'alt+x'
print('Hotkey set as:', shortcut)


def on_triggered():
    print(text_to_print)


keyboard.add_hotkey(shortcut, on_triggered)

print("Press ESC to stop.")
keyboard.wait('esc')
