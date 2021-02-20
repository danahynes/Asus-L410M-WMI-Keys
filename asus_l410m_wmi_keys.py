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

# get cam vendor/product id
webcam_found = False
with open('/proc/bus/input/devices', 'r') as f:
    lines = f.readlines()

    # walk through the file backward (vendor and product come before the name)
    for line in reversed(lines):
        if "WEBCAM" in line.upper():
            webcam_found = True
            continue
        if webcam_found:
            parts = line.split(" ")
            vendor = parts[2]
            vendor = vendor.split("=")
            vendor = vendor[1]
            product = parts[3]
            product = product.split("=")
            product = product[1]
            break

# get cam bus/device
if webcam_found:

    # find all matching vendors
    vendor_list = []
    possible_ids = os.listdir("/sys/bus/usb/devices/")
    for id in possible_ids:
        newfile = "/sys/bus/usb/devices/" + id + "/idVendor"
        if os.path.exists(newfile):
            with open(newfile, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if re.search(vendor, line):
                        vendor_list.append(id)
                        break

    # find all matching products in all matching vendors
    product_list = []
    for id in vendor_list:
        newfile = "/sys/bus/usb/devices/" + id + "/idProduct"
        if os.path.exists(newfile):
            with open(newfile, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if re.search(product, line):
                        product_list.append(id)
                        break

# get cam_id
cam_id = -1

# make sure there is only one camera entry
if len(product_list) > 1:
    print("More than one camera found, disabling camera key")
elif len(product_list) == 0:
    print("No camera found, disabling camera key")
else:

    # grab the only matchng vendor/product
    cam_id = product_list[0]

# get current cam state
cam_state = False
if cam_id != -1:
    cam_file = "/sys/bus/usb/devices/" + cam_id + "/bConfigurationValue"
    if os.path.exists(cam_file):
        with open(cam_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "1" in line:
                    cam_state = True
                    break

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
            break

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
# N.B. this grabs ALL WMI keys, but the ones we don't explicitily handle will
# get bubbled up to the asus-nb-wmi driver, so the system can still see them
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

    # look at each event in the wmi keyboard pipe
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
            except OSError as e:
                pass

        # not our key
        else:
            pass

    # don't eat all cpu!
    time.sleep(0.1)

# release Keyboard
wmi_kbd.ungrab()

# close file descriptor (pipe) we opened
fd_wmi_kbd.close()

# -)
