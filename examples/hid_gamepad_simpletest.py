# SPDX-FileCopyrightText: 2023 Neradoc
# SPDX-License-Identifier: MIT

import board
import time
import usb_hid
from hid_gamepad.simple import Gamepad

gp = Gamepad(usb_hid.devices)

while True:
    for button in range(1, 9):
        gp.press_buttons(button)
        time.sleep(0.5)
        gp.release_buttons(button)
        time.sleep(0.5)
