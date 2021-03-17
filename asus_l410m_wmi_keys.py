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

# find WMI keyboard
wmi_kbd_found = False
wmi_kbd_id = -1
wmi_kbd = None

# check if file exists
if os.path.exists('/proc/bus/input/devices'):

    # read file
    with open('/proc/bus/input/devices', 'r') as f:
        lines = f.readlines()

        # walk through the file to find hotkeys device
        for line in lines:
            if 'NAME="ASUS WMI HOTKEYS"' in line.upper():

                # keep walking
                wmi_kbd_found = True
                continue

            # found WMI device
            if wmi_kbd_found:

                # keep walking to find handlers line
                if 'HANDLERS' in line.upper():

                    # save everything after equals sign
                    handlers = line.split('=')[-1]

                    # get array of handlers
                    handler_array = handlers.split(' ')

                    # find event
                    for handler in handler_array:
                        if 'EVENT' in handler.upper():
                            event = handler.upper().split('EVENT')

                            # save it
                            wmi_kbd_id = event[-1]
                            break

                    # no more to do here
                    break

# no keyboard, no laundry
if not wmi_kbd_found or wmi_kbd_id == -1:
    logging.debug('WMI keyboard not found, freaking out...')
    sys.exit(1)

# try to connect to keyboard
if os.path.exists('/dev/input/event' + str(wmi_kbd_id)):

    # open a file descriptor (pipe) for the WMI keyboard
    fd_wmi_kbd = open('/dev/input/event' + str(wmi_kbd_id), 'rb')

    # set file descriptor (pipe) to non-blocking
    try:
        fcntl.fcntl(fd_wmi_kbd, fcntl.F_SETFL, os.O_NONBLOCK)
    except ValueError as err:
        pass

    # get a device object (end point) for the file descriptor (pipe)
    try:
        wmi_kbd = libevdev.Device(fd_wmi_kbd)
    except libevdev.device.InvalidFileError as err:
        pass

# no keyboard, no laundry
if wmi_kbd == None:
    logging.debug('Could not open connection to keyboard, freaking out...')
    sys.exit(1)

# create a fake keyboard for the keys
dev_fake_kbd = libevdev.Device()
dev_fake_kbd.name = 'Asus_L410M_WMI_Keys'
dev_fake_kbd.enable(libevdev.EV_KEY.KEY_LEFTSHIFT)
dev_fake_kbd.enable(libevdev.EV_KEY.KEY_LEFTMETA)
dev_fake_kbd.enable(libevdev.EV_KEY.KEY_R)
dev_fake_kbd.enable(libevdev.EV_KEY.KEY_T)
fake_kbd = dev_fake_kbd.create_uinput_device()

# constants
# TODO: find an easier way to get these besides dmesg
KEY_WMI_CAMERA = 0x85
KEY_WMI_MYASUS = 0x86

# main loop
while True:

    # look at each event in the wmi keyboard pipe
    for event in wmi_kbd.events():

        # if it's the camera key
        if event.value == KEY_WMI_CAMERA:
            logging.debug('Camera key pressed')
            try:

                # press Shift
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_LEFTSHIFT, 1),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)

                # press Meta
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_LEFTMETA, 1),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)

                # press R
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_R, 1),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)

                # release R
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_R, 0),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)

                # release Meta
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_LEFTMETA, 0),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)

                # release Shift
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_LEFTSHIFT, 0),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)
            except OSError as err:
                logging.debug(str(err))

        # if it's the "MyAsus" key
        elif event.value == KEY_WMI_MYASUS:
            logging.debug('MyAsus key pressed')
            try:

                # press Shift
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_LEFTSHIFT, 1),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)

                # press Meta
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_LEFTMETA, 1),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)

                # press T
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_T, 1),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)

                # release T
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_T, 0),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)

                # release Meta
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_LEFTMETA, 0),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)

                # release Shift
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_LEFTSHIFT, 0),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)
            except OSError as err:
                logging.debug(str(err))

        # not our key
        else:
            pass

    # don't eat all cpu!
    time.sleep(0.1)

# close file descriptor (pipe) we opened
fd_wmi_kbd.close()

# -)
