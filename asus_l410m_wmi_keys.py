#!/usr/bin/env python3
#------------------------------------------------------------------------------#
# Filename: asus_l410m_wmi_keys.py                               /          \  #
# Project : Asus_L410M_WMI_Keys                                 |     ()     | #
# Date    : 02/17/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

#imports
import fcntl
import libevdev
import logging
import os
import sys
import time

# set up logging
logging.basicConfig(filename = '/var/log/asus_l410m_wmi_keys.log',
    level = logging.DEBUG, format = '%(asctime)s - %(message)s')

# just let users know its starting
logging.debug('---------------------------------------------------------------')
logging.debug('Starting script')

#-------------------------------------------------------------------------------
# helper functions
#-------------------------------------------------------------------------------

# returns a libevdev device for the given name
def get_device(device_name):

    # assume no device
    device_found = False
    device_id = -1
    device = None

    # check if file exists
    if os.path.exists('/proc/bus/input/devices'):

        # read file
        with open('/proc/bus/input/devices', 'r') as f:
            lines = f.readlines()

            # walk through the file
            for line in lines:
                if device_name.upper() in line.upper():

                    # keep walking
                    device_found = True
                    continue

                # found keyboard
                if device_found:

                    # keep walking to find handlers line
                    if 'HANDLERS' in line.upper():

                        # get array of handlers
                        handlers = line.split('=')[-1]

                        # get array of handlers
                        handler_array = handlers.split(' ')

                        # find event
                        for handler in handler_array:
                            if 'EVENT' in handler.upper():
                                event = handler.upper().split('EVENT')

                                # save it
                                device_id = event[-1]
                                break

                        # no more to do here
                        break

    # no device, no laundry
    if not device_found or device_id == -1:
        return None

    # try to connect to device
    if os.path.exists('/dev/input/event' + str(device_id)):

        # create a file descriptor (pipe) for the keyboard
        fd_device = open('/dev/input/event' + str(device_id), 'rb')

        # set file descriptor (pipe) to non-blocking
        try:
            fcntl.fcntl(fd_device, fcntl.F_SETFL, os.O_NONBLOCK)
        except ValueError as err:
            logging.debug(str(err))
            return None

        # get a device object (end point) for the file descriptor (pipe)
        try:
            device = libevdev.Device(fd_device)
        except libevdev.device.InvalidFileError as err:
            logging.debug(str(err))
            return None

        # return found (or not found) device
        return device

#-------------------------------------------------------------------------------
# Initialize
#-------------------------------------------------------------------------------

# get WMI keyboard
wmi_keyboard = get_device('HOTKEYS')

# no device, no laundry
if wmi_keyboard == None:
    logging.debug('Could not find WMI keyboard, freaking out...')
    sys.exit(1)

#-------------------------------------------------------------------------------
# THIS IS WHERE YOU ADD/EDIT UNMAPPED KEYS
#-------------------------------------------------------------------------------

KEY_WMI_CAMERA = 0x85
KEY_WMI_MYASUS = 0x86

# map scancode to actual keystrokes
key_wmi_camera = [
    KEY_WMI_CAMERA,
    libevdev.EV_KEY.KEY_LEFTSHIFT,
    libevdev.EV_KEY.KEY_LEFTMETA,
    libevdev.EV_KEY.KEY_R
]

# map scancode to actual keystrokes
key_wmi_myasus = [
    KEY_WMI_MYASUS,
    libevdev.EV_KEY.KEY_LEFTSHIFT,
    libevdev.EV_KEY.KEY_LEFTMETA,
    libevdev.EV_KEY.KEY_T
]

# array of all remapped keys
keys_wmi = [
    key_wmi_camera,
    key_wmi_myasus
]

#-------------------------------------------------------------------------------
# DONE
#-------------------------------------------------------------------------------

# create a fake keyboard to send keys
# NB: devices found using get_device() are read-only so create a new device
# that we can write to
dev_wmi_kbd = libevdev.Device()
dev_wmi_kbd.name = 'Asus_L410M_WMI_Keys'
for key in keys_wmi:
    keys_to_enable = key[1:]
    for key_to_enable in keys_to_enable:
        dev_wmi_kbd.enable(key_to_enable)
new_wmi_kbd = dev_wmi_kbd.create_uinput_device()

#-------------------------------------------------------------------------------
# Main loop
#-------------------------------------------------------------------------------

while True:

    # look at each event in the wmi keyboard pipe
    for e in wmi_keyboard.events():

        # loop through our keys
        for key_wmi in keys_wmi:

            # if it's one of ours
            if (e.value == key_wmi[0]):

                # get the mapped keystrokes to send
                keys_to_send = key_wmi[1:]

                # for each key, send the "key down" message
                for key_to_send in keys_to_send:
                    events = [
                        libevdev.InputEvent(key_to_send, 1)
                    ]
                    new_wmi_kbd.send_events(events)

                    # pause a bit between keys
                    time.sleep(0.1)

                # for each key in reverse, release it
                for key_to_send in reversed(keys_to_send):
                    events = [
                        libevdev.InputEvent(key_to_send, 0)
                    ]
                    new_wmi_kbd.send_events(events)

                    # pause a bit between keys
                    time.sleep(0.1)

                # send the "event complete" message
                events = [
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                new_wmi_kbd.send_events(events)

    # give somebody else a chance will ya!
    time.sleep(0.1)

# -)
