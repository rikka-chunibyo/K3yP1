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
    13: Keycode.ENTER,
    127: Keycode.BACKSPACE,
    9: Keycode.TAB,
    27: "ESC",  # Escape sequences, needs handling for multi-byte keys
}

arrow_keys = {
    218: Keycode.UP_ARROW,
    217: Keycode.DOWN_ARROW,
    216: Keycode.LEFT_ARROW,
    215: Keycode.RIGHT_ARROW,
}

# Read buffer for handling multi-byte sequences (e.g., ESC + '[' + 'A' for Up Arrow)
esc_sequence = []

while True:
    if uart.in_waiting:
        byte_read = uart.read(1)
        if byte_read:
            char_code = ord(byte_read)

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

            # Handle predefined mappings
            if char_code in key_map:
                keyboard.send(key_map[char_code])

            # Handle normal printable characters
            elif 32 <= char_code <= 126:  # Standard ASCII printable characters
                char = chr(char_code)
                if 'a' <= char <= 'z':  # Lowercase letters
                    keyboard.send(getattr(Keycode, char.upper()))
                elif 'A' <= char <= 'Z':  # Uppercase letters (send Shift)
                    keyboard.press(Keycode.SHIFT, getattr(Keycode, char))
                    keyboard.release_all()
                elif '0' <= char <= '9':  # Numbers
                    keyboard.send(getattr(Keycode, char))
                else:
                    pass  # Ignore unmapped characters
