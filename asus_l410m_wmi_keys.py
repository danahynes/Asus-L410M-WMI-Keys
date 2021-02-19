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
import os
import re
import time

# constants
# TODO: find an easier way to get these besides dmesg
KEY_WMI_CAMERA = 133
KEY_WMI_MYASUS = 134

# get cam_id
cam_id = -1
with open('/proc/bus/input/devices', 'r') as f:
    webcam_found = False
    lines = f.readlines()

    # walk through the file backward (vendor and product come before the name)
    for line in reversed(lines):
        if "WEBCAM" in line.upper():
            webcam_found = True
            continue
        if webcam_found:
            webcam_found = False
            parts = line.split(" ")
            vendor = parts[2]
            vendor = vendor.split("=")
            vendor = vendor[1]
            product = parts[3]
            product = product.split("=")
            product = product[1]

            # find all matching vendors
            list = []
            for file in os.listdir("/sys/bus/usb/devices/"):
                newfile = "/sys/bus/usb/devices/" + file + "/idVendor"
                if os.path.exists(newfile):
                    with open(newfile, "r") as f2:
                        lines2 = f2.readlines()
                        for line2 in lines2:
                            if re.search(vendor, line2):
                                list.append(file)

            # find all matching products
            list2 = []
            for file in list:
                newfile = "/sys/bus/usb/devices/" + file + "/idProduct"
                if os.path.exists(newfile):
                    with open(newfile, "r") as f2:
                        lines2 = f2.readlines()
                        for line2 in lines2:
                            if re.search(product, line2):
                                list2.append(file)

# make sure there is only one camera entry
if len(list2) > 1:
    print("More than one camera found, disabling camera key...")
elif len(list2) == 0:
    print("No camera found, disabling camera key...")
else:

    # grab the only matchng vendor/product
    cam_id = list2[0]

# get current cam state
cam_state = False
if cam_id != -1:
    cam_file = "/sys/bus/usb/devices/" + cam_id + "/bConfigurationValue"
    if (os.path.exists(cam_file)):
        with open(cam_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "1" in line:
                    cam_state = True

# find WMI keyboard
wmi_kbd_id = -1
with open('/proc/bus/input/devices', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if "Sysfs=/devices/platform/asus-nb-wmi/input/" in line:
            parts = line.split("/")
            part = parts[-1]
            parts = part.split("input")
            wmi_kbd_id = parts[1].rstrip()

# make sure we found the keyboard
if wmi_kbd_id == -1:
    print("WMI keyboard not found, freaking out...")
    sys.exit(1)

# create a file descriptor (pipe) for the WMI keyboard
fd_wmi_kbd = open('/dev/input/event' + str(wmi_kbd_id), 'rb')

# set file descriptor (pipe) to non-blocking
fcntl.fcntl(fd_wmi_kbd, fcntl.F_SETFL, os.O_NONBLOCK)

# get a device object (end point) for the file descriptor (pipe)
wmi_kbd = libevdev.Device(fd_wmi_kbd)

# prevent the keys from sending their unmapped (0x0) codes to the system
wmi_kbd.grab()

# create a fake keyboard for the "MyAsus" key
dev_fake_kbd = libevdev.Device()
dev_fake_kbd.name = "Asus_L410M_WMI_Keys"
dev_fake_kbd.enable(libevdev.EV_KEY.KEY_LEFTSHIFT)
dev_fake_kbd.enable(libevdev.EV_KEY.KEY_LEFTMETA)
dev_fake_kbd.enable(libevdev.EV_KEY.KEY_R)
dev_fake_kbd.enable(libevdev.EV_KEY.KEY_T)
fake_kbd = dev_fake_kbd.create_uinput_device()

# main loop
while True:

    # look at each event in the pipe
    for e in wmi_kbd.events():

        # if it's the camera key
        if e.value == KEY_WMI_CAMERA:

            # if we found the camera
            if cam_id != -1:

                # toggle the camera state
                cam_state = not cam_state

                # get the proper file for the cam
                cam_file = open("/sys/bus/usb/devices/" + cam_id +
                    "/bConfigurationValue", "w+")

                # turn cam on
                if cam_state:
                    cam_file.write("1")

                # turn cam off
                else:
                    cam_file.write("0")

                # done with cam file
                cam_file.flush()
                cam_file.close()

            # no camera, map to Shift-Meta-R
            else:
                try:

                    # press Shift
                    events = [
                        libevdev.InputEvent(libevdev.EV_KEY.KEY_LEFTSHIFT, 1),
                        libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                    ]
                    fake_kbd.send_events(events)

                    # press Cmd
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

                    # release Cmd
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
                except OSError as e:
                    pass

        # if it's the "MyAsus" key
        elif e.value == KEY_WMI_MYASUS:
            try:

                # press Shift
                events = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_LEFTSHIFT, 1),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)
                ]
                fake_kbd.send_events(events)

                # press Cmd
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

                # release Cmd
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
            except OSError as e:
                pass

    # don't eat all cpu!
    time.sleep(0.1)

# release Keyboard
wmi_kbd.ungrab()

# close file descriptor (pipe) we opened
fd_wmi_kbd.close()

# -)
