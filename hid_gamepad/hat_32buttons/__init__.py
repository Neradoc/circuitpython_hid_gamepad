# SPDX-FileCopyrightText: 2018 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`Gamepad`
====================================================

* Author(s): Dan Halbert, Neradoc, werpu on github

Borrowed from:
https://gist.github.com/werpu/15d4166aa8d999af0d12f0c9d8a9eccf
"""

import struct
import time

from adafruit_hid import find_device


NUM_BUTTONS = 32


class Gamepad:
    """Emulate a generic gamepad controller with 32 buttons,
    numbered 1-32, and two joysticks, one controlling
    ``x` and ``y`` values, and the other controlling ``z`` and
    ``r_z`` (z rotation or ``Rz``) values.

    The joystick values could be interpreted
    differently by the receiving program: those are just the names used here.
    The joystick values are in the range -127 to 127."""

    def __init__(self, devices):
        """Create a Gamepad object that will send USB gamepad HID reports.

        Devices can be a list of devices that includes a gamepad device or a gamepad device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._gamepad_device = find_device(devices, usage_page=0x1, usage=0x05)

        # Reuse this bytearray to send mouse reports.
        # Typically controllers start numbering buttons at 1 rather than 0.
        # report[0] buttons 1-8 (LSB is button 1)
        # report[1] buttons 9-16
        # report[2] buttons 17-24
        # report[3] buttons 24-32
        # report[4] joystick 0 x: -127 to 127
        # report[5] joystick 0 y: -127 to 127
        # report[6] joystick 1 x: -127 to 127
        # report[7] joystick 1 y: -127 to 127
        # report[8] joystick 1 hat/d-pad
        self._report = bytearray(9)

        # Remember the last report as well, so we can avoid sending
        # duplicate reports.
        self._last_report = bytearray(9)

        # Store settings separately before putting into report. Saves code
        # especially for buttons.
        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._joy_z = 0
        self._joy_r_z = 0
        self._hat = 0

        # Send an initial report to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

    def press_buttons(self, *buttons):
        """Press and hold the given buttons."""
        for button in buttons:
            self._buttons_state |= 1 << self._validate_button_number(button) - 1
        self._send()

    def release_buttons(self, *buttons):
        """Release the given buttons."""
        for button in buttons:
            self._buttons_state &= ~(1 << self._validate_button_number(button) - 1)
        self._send()

    def release_all_buttons(self):
        """Release all the buttons."""

        self._buttons_state = 0
        self._send()

    def click_buttons(self, *buttons):
        """Press and release the given buttons."""
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def move_joysticks(self, x=None, y=None, z=None, r_z=None):
        """Set and send the given joystick values.
        The joysticks will remain set with the given values until changed

        One joystick provides ``x`` and ``y`` values,
        and the other provides ``z`` and ``r_z`` (z rotation).
        Any values left as ``None`` will not be changed.

        All values must be in the range -127 to 127 inclusive.

        Examples::

            # Change x and y values only.
            gp.move_joysticks(x=100, y=-50)

            # Reset all joystick values to center position.
            gp.move_joysticks(0, 0, 0, 0)
        """
        if x is not None:
            self._joy_x = self._validate_joystick_value(x)
        if y is not None:
            self._joy_y = self._validate_joystick_value(y)
        if z is not None:
            self._joy_z = self._validate_joystick_value(z)
        if r_z is not None:
            self._joy_r_z = self._validate_joystick_value(r_z)
        self._send()

    def hat(self, *, button=None, up=None, down=None, left=None, right=None):
        if button is not None:
            self._hat = self._hat & 0b01111 | int(button) << 4
        if up is not None:
            self._hat = self._hat & 0b10111 | int(up) << 3
        if down is not None:
            self._hat = self._hat & 0b11011 | int(down) << 2
        if left is not None:
            self._hat = self._hat & 0b01101 | int(left) << 1
        if right is not None:
            self._hat = self._hat & 0b01110 | int(right)
        self._send()

    def reset_all(self):
        """Release all buttons and set joysticks to zero."""
        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._joy_z = 0
        self._joy_r_z = 0
        self._hat = 0
        self._send(always=True)

    def _send(self, always=False):
        """Send a report with all the existing settings.
        If ``always`` is ``False`` (the default), send only if there have been changes.
        """
        struct.pack_into(
            "<IbbbbB", # < little endian, I 32-bit (4-byte) field for 32 buttons, b signed 8-bit integer, B unsigned 8-bit integer
            self._report,
            0,
            self._buttons_state,
            self._joy_x,
            self._joy_y,
            self._joy_z,
            self._joy_r_z,
            self._hat & 0b11111
        )

        if always or self._last_report != self._report:
            self._gamepad_device.send_report(self._report)
            # Remember what we sent, without allocating new storage.
            self._last_report[:] = self._report

    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= NUM_BUTTONS:
            raise ValueError("Button number must in range 1 to {NUM_BUTTONS}")
        return button

    @staticmethod
    def _validate_joystick_value(value):
        if not -127 <= value <= 127:
            raise ValueError("Joystick value must be in range -127 to 127")
        return value
