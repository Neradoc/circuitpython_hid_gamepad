"""
Borrowed from:
https://gist.github.com/werpu/15d4166aa8d999af0d12f0c9d8a9eccf
"""
import usb_hid

# This is only one example of a gamepad descriptor, and may not suit your needs.
GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09, 0x05,  # Usage (Game Pad)
    0xA1, 0x01,  # Collection (Application)
    0x85, 0x04,  #   Report ID (4)
    0x05, 0x09,  #   Usage Page (Button)
    0x19, 0x01,  #   Usage Minimum (Button 1)
    0x29, 0x20,  #   Usage Maximum (Button 32)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x75, 0x01,  #   Report Size (1)
    0x95, 0x20,  #   Report Count (32)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x01,  #   Usage Page (Generic Desktop Ctrls)
    0x15, 0x81,  #   Logical Minimum (-127)
    0x25, 0x7F,  #   Logical Maximum (127)
    0x09, 0x30,  #   Usage (X)
    0x09, 0x31,  #   Usage (Y)
    0x09, 0x32,  #   Usage (Z)
    0x09, 0x35,  #   Usage (Rz)
    0x75, 0x08,  #   Report Size (8)
    0x95, 0x04,  #   Report Count (4)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)

    ## hat switch 1 byte extra but only 5 bit used
    # https://stackoverflow.com/questions/60132199/cannot-figure-out-how-to-send-data-to-hat-switch-from-stm32f103c8-to-pc-via-usb
    0x05, 0x01,  # Usage Page: Generic Desktop
    0x09, 0x39,  # Usage: Hat Switch,
    0x15, 0x00,  # Logical Min: 0
    0x25, 0x07,  # Logical Max: 7
    0x46, 0x3B, 0x01, # Physical Maximum: 315 degrees (Optional)
    0x75, 0x08,  # ReportSize: 8
    0x95, 0x01,  # Report Count: 1
    0x65, 0x14,  # Unit: English Rotation / Angular Position 1 degree(Optional)
    0x81, 0x42,  # Input: Data, Var, Abs, Null State

    0xC0,        # End Collection
))

gamepad_descriptor = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(4,),           # Descriptor uses report ID 4.
    in_report_lengths=(9,),    # This gamepad sends 9 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)
