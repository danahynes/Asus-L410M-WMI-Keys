from fcntl import fcntl, F_SETFL
from libevdev import Device, InputEvent, EV_KEY, EV_SYN
from os import O_NONBLOCK
from time import sleep
# import subprocess
import os
import re

with open('/proc/bus/input/devices', 'r') as f:

    found = False
    lines = f.readlines()
    for line in reversed(lines):
        if "WEBCAM" in line.upper():
            print(line)
            found = True
            continue
        if found:
            print(line)
            found = False
            parts = line.split(" ")
            print(parts)
            vendor = parts[2]
            vendor = vendor.split("=")
            vendor = vendor[1]
            print(vendor)
            product = parts[3]
            product = product.split("=")
            product = product[1]
            print(product)
            # parts = line.split("/")
            # part = parts[-1]
            # print(part)
            # parts = part.split("input")
            # print(parts[1])
            
            list = []
            for file in os.listdir("/sys/bus/usb/devices/"):
                newfile = "/sys/bus/usb/devices/" + file + "/idVendor"
                if os.path.exists(newfile):
                    with open(newfile, "r") as f2:
                        lines2 = f2.readlines()
                        for line2 in lines2:
                            if re.search(vendor, line2):
                                list.append(file)

            list2 = []
            for file in list:
                newfile = "/sys/bus/usb/devices/" + file + "/idProduct"
                if os.path.exists(newfile):
                    with open(newfile, "r") as f2:
                        lines2 = f2.readlines()
                        for line2 in lines2:
                            if re.search(product, line2):
                                list2.append(file)



            print(list2)               #
                # res = subprocess.Popen(['grep', vendor, newfile], stdout= subprocess.PIPE)
                # print("res: " + str(res))
            # hosts = subprocess.Popen(['grep', vendor, '"/sys/bus/usb/devices/*/idVendor"'], stdout= subprocess.PIPE)
            # print(hosts)
