from libevdev import Device
from fcntl import fcntl, F_SETFL
from time import sleep
from os import O_NONBLOCK

keyboard = 6
cam = True

fd_keyboard = open('/dev/input/event' + str(keyboard), 'rb')
fcntl(fd_keyboard, F_SETFL, O_NONBLOCK)
d_keyboard = Device(fd_keyboard)

while True:

    for e in d_keyboard.events():
        #print(e)
        if e.value == 133:
            cam = not cam
            cam_file = open("/sys/bus/usb/devices/1-5/bConfigurationValue", "w")
            if cam:
                cam_file.write("1")
                print("on")
            else:
                cam_file.write("0")
                print("off")
            cam_file.close()

        elif e.value == 134:
            print("F12")
    sleep(0.1)

fd_keyboard.close()
