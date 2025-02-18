import usb_cdc
import usb_hid

usb_cdc.enable(console=True, data=True)  # Enable serial data channel
usb_hid.enable((usb_hid.Device.KEYBOARD,))  # Enable USB keyboard
