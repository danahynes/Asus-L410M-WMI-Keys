from fcntl import fcntl, F_SETFL
from libevdev import Device, InputEvent, EV_KEY, EV_SYN
from os import O_NONBLOCK
from time import sleep

with open('/proc/bus/input/devices', 'r') as f:

    lines = f.readlines()
    for line in lines:
        if "Sysfs=/devices/platform/asus-nb-wmi/input/" in line:
            print(line)
            parts = line.split("/")
            part = parts[-1]
            print(part)
            parts = part.split("input")
            print(parts[1])
