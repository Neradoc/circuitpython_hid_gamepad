from hid_gamepad.simple.boot import gamepad_descriptor
import usb_hid

usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.MOUSE,
     usb_hid.Device.CONSUMER_CONTROL,
     gamepad_descriptor)
)

# Only use the gamepad:
# usb_hid.enable((gamepad_descriptor,))
