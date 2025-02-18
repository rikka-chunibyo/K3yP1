import board
import busio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Set up serial communication over UART
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)  # Adjust pins as needed

# Set up HID keyboard
keyboard = Keyboard(usb_hid.devices)

# Mapping of received character codes to HID keycodes
key_map = {
    13: Keycode.ENTER,      # Enter key
    127: Keycode.BACKSPACE, # Backspace key
    9: Keycode.TAB,         # Tab key
    27: "ESC",              # Escape sequences (handled separately)
    32: Keycode.SPACE,      # Space key
}

arrow_keys = {
    218: Keycode.UP_ARROW,
    217: Keycode.DOWN_ARROW,
    216: Keycode.LEFT_ARROW,
    215: Keycode.RIGHT_ARROW,
}

esc_sequence = []  # Buffer for handling multi-byte sequences (e.g., arrow keys)

while True:
    if uart.in_waiting:
        byte_read = uart.read(1)
        if byte_read:
            char_code = ord(byte_read)

            print(f"Received: {char_code}")  # Debugging output

            # Handle Escape sequences (Arrow keys, function keys)
            if esc_sequence or char_code == 27:
                esc_sequence.append(char_code)

                if len(esc_sequence) == 3:  # Expecting ESC + '[' + 'A' format
                    if esc_sequence[1] == 91:  # '[' character (start of arrow sequence)
                        arrow_char = esc_sequence[2]
                        if arrow_char in arrow_keys:
                            keyboard.send(arrow_keys[arrow_char])

                    esc_sequence = []  # Reset sequence after processing
                continue

            # Handle predefined mappings (Enter, Backspace, Tab, Space, etc.)
            if char_code in key_map:
                keyboard.send(key_map[char_code])

            # Handle Ctrl + [A-Z] (ASCII 1-26)
            elif 1 <= char_code <= 26:
                ctrl_char = chr(char_code + 64)  # Convert to uppercase letter
                if hasattr(Keycode, ctrl_char):
                    keyboard.press(Keycode.CONTROL, getattr(Keycode, ctrl_char))
                    keyboard.release_all()

            # Handle normal printable characters
            elif 32 <= char_code <= 126:
                char = chr(char_code)

                if 'a' <= char <= 'z':  # Lowercase letters
                    keyboard.send(getattr(Keycode, char.upper()))
                elif 'A' <= char <= 'Z':  # Uppercase letters (requires Shift)
                    keyboard.press(Keycode.SHIFT, getattr(Keycode, char))
                    keyboard.release_all()
                elif '0' <= char <= '9':  # Numbers
                    keyboard.send(getattr(Keycode, char))
                elif char_code in key_map:  # Symbols like Space
                    keyboard.send(key_map[char_code])
                else:
                    print(f"Unhandled key: {char_code}")  # Debugging output
