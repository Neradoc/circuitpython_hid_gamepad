# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# midi_inoutdemo - demonstrates receiving and sending MIDI events

import board
import digitalio
import analogio
import usb_hid

from hid_gamepad.hat_32buttons import Gamepad

gp = Gamepad(usb_hid.devices)

import board
import keypad

from adafruit_is31fl3731.keybow2040 import Keybow2040 as Display
from rainbowio import colorwheel

pins = [getattr(board, f"SW{i}") for i in range(16)]
keys = keypad.Keys(pins, value_when_pressed=False, pull=True)
keycolor = [0] * 16
display = Display(board.I2C())

def xy_to_num(x, y):
    num = y + 4 * (3 - x)
    return num

colors = [
    (0,0,255), None, None, None,
    None, None, None, None,
    None, None, (0,255,0), None,
    None, (0,255,0), (0,255,0), (0,255,0),
]

for x in range(4):
    for y in range(4):
        bnm = xy_to_num(x, y)
        color = colors[bnm]
        if color:
            display.pixelrgb(x, y, color[0], color[1], color[2])
        else:
            display.pixelrgb(x, y, 0, 0, 0)

while True:
    event = keys.events.get()
    if event:
        bnm = event.key_number
        y, x = divmod(bnm, 4)
        #keycolor[bnm] += 1
        #display.pixelrgb(x, y, *colorwheel(keycolor[bnm]*8).to_bytes(3, "big"))
        if (x,y) == (1,2):
            if event.pressed:
                gp.hat(up=True)
            else:
                gp.hat(up=False)
        elif (x,y) == (0,1):
            if event.pressed:
                gp.hat(left=True)
            else:
                gp.hat(left=False)
        elif (x,y) == (0,2):
            if event.pressed:
                gp.hat(down=True)
            else:
                gp.hat(down=False)
        elif (x,y) == (0,3):
            if event.pressed:
                gp.hat(right=True)
            else:
                gp.hat(right=False)
        elif (x,y) == (3,0):
            if event.pressed:
                gp.hat(button=True)
            else:
                gp.hat(button=False)
        else:
            if event.pressed:
                gp.press_buttons(bnm + 1)
            else:
                gp.release_buttons(bnm + 1)

        print(gp._report)

