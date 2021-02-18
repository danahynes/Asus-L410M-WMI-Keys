# Asus_L410M_WMI_Keys
This small program runs at boot and gives you access to the keys on the keyboard that aren't handled by the current asus-nb-wmi driver.

On my laptop (a 2020 Asus L410M) these are the camera toggle key (same as F10) and the "Launch MyAsus" key (same as F12).

I banged my head against a wall for a few hours until I found a solution to this. At first I thought the asus-nb-wmi driver was swallowing events for keys it did not recognize (actually some programs, like xev, could see them being pressed and released but they just had 0x0 scancodes). But then I realized the asus-nb-wmi driver was logging them in dmesg as unknown keys, but with unique scancodes. Turns out that the python library libevdev can read the scancodes from the keyboard before the asus-nb-wmi driver throws them away.

For the camera key, I am "poking" a value into a file that the camera watches to see if it should be enabled.

Note that this is NOT a one-to-one hardware switch for the webcam. It will turn the webcam off if you're using an app that is using the webcam, but it won't turn back on if the app is still running. Also if you do use the key while the camera is in use, there is an issue where the system file gets out of sync (I believe the app has a lock on the file) and you may have to press the button a few times with all apps closed to re-sync it. I'm working on it, but for now, "it mostly works".

As for the "MyAsus" key, it presents itself as Shift-Meta-T. You should be able to map it to something useful using your system's keyboard shortcuts. I'm currently using it to launch Chromium and it works perfectly.

# Installing

To install, clone the git repo:
```
foo@bar:~$ cd ~/Downloads
foo@bar:~$ git clone https://github.com/danahynes/Asus_L410M_WMI_Keys.git
foo@bar:~$ cd Asus_L410M_WMI_keys
```

You WILL need to find the cam_id and the key scancodes and edit Asus_L410M_WMI_Keys.py before you install. See note below!
Once you do that, you can install by:
```
foo@bar:~$ sudo ./install.sh
```
You can also download the [latest release](http://github.com/danahynes/Asus_L410M_WMI_Keys/releases), unzip it, set the cam_id and scancodesin Asus_L410M_WMI_Keys.py, and run the install.sh file from there.

# Finding the cam_id and KEY_WMI_* values

Finding the cam_id is a little hard. Lets start with:
```
foo@bar:~$ cat /proc/bus/input/devices
```

Here is my output:
```
I: Bus=0019 Vendor=0000 Product=0001 Version=0000
N: Name="Power Button"
P: Phys=PNP0C0C/button/input0
S: Sysfs=/devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:03/PNP0C09:01/PNP0C0C:00/input/input0
U: Uniq=
H: Handlers=kbd event0
B: PROP=0
B: EV=3
B: KEY=10000000000000 0

I: Bus=0019 Vendor=0000 Product=0005 Version=0000
N: Name="Lid Switch"
P: Phys=PNP0C0D/button/input0
S: Sysfs=/devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:03/PNP0C09:01/PNP0C0D:01/input/input1
U: Uniq=
H: Handlers=event1
B: PROP=0
B: EV=21
B: SW=1

I: Bus=0019 Vendor=0000 Product=0001 Version=0000
N: Name="Power Button"
P: Phys=PNP0C0C/button/input0
S: Sysfs=/devices/LNXSYSTM:00/LNXSYBUS:00/PNP0C0C:01/input/input2
U: Uniq=
H: Handlers=kbd event2
B: PROP=0
B: EV=3
B: KEY=10000000000000 0

I: Bus=0011 Vendor=0001 Product=0001 Version=ab83
N: Name="AT Translated Set 2 keyboard"
P: Phys=isa0060/serio0/input0
S: Sysfs=/devices/platform/i8042/serio0/input/input3
U: Uniq=
H: Handlers=sysrq kbd event3 leds
B: PROP=0
B: EV=120013
B: KEY=402000000 3803078f800d001 feffffdfffefffff fffffffffffffffe
B: MSC=10
B: LED=7

I: Bus=0019 Vendor=0000 Product=0006 Version=0000
N: Name="Video Bus"
P: Phys=LNXVIDEO/video/input0
S: Sysfs=/devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/LNXVIDEO:00/input/input4
U: Uniq=
H: Handlers=kbd event4
B: PROP=0
B: EV=3
B: KEY=3e000b00000000 0 0 0

I: Bus=0019 Vendor=0000 Product=0000 Version=0000
N: Name="Asus WMI hotkeys"
P: Phys=asus-nb-wmi/input0
S: Sysfs=/devices/platform/asus-nb-wmi/input/input6
U: Uniq=
H: Handlers=rfkill kbd event6
B: PROP=0
B: EV=100013
B: KEY=1000000080000 0 0 0 0 181606f00900000 8200027801701000 e000000000000 0
B: MSC=10

I: Bus=0000 Vendor=0000 Product=0000 Version=0000
N: Name="HDA Intel PCH Headphone"
P: Phys=ALSA
S: Sysfs=/devices/pci0000:00/0000:00:0e.0/sound/card0/input7
U: Uniq=
H: Handlers=event7
B: PROP=0
B: EV=21
B: SW=4

I: Bus=0000 Vendor=0000 Product=0000 Version=0000
N: Name="HDA Intel PCH HDMI/DP,pcm=3"
P: Phys=ALSA
S: Sysfs=/devices/pci0000:00/0000:00:0e.0/sound/card0/input8
U: Uniq=
H: Handlers=event8
B: PROP=0
B: EV=21
B: SW=140

I: Bus=0000 Vendor=0000 Product=0000 Version=0000
N: Name="HDA Intel PCH HDMI/DP,pcm=7"
P: Phys=ALSA
S: Sysfs=/devices/pci0000:00/0000:00:0e.0/sound/card0/input9
U: Uniq=
H: Handlers=event9
B: PROP=0
B: EV=21
B: SW=140

I: Bus=0000 Vendor=0000 Product=0000 Version=0000
N: Name="HDA Intel PCH HDMI/DP,pcm=8"
P: Phys=ALSA
S: Sysfs=/devices/pci0000:00/0000:00:0e.0/sound/card0/input10
U: Uniq=
H: Handlers=event10
B: PROP=0
B: EV=21
B: SW=140

I: Bus=0000 Vendor=0000 Product=0000 Version=0000
N: Name="HDA Intel PCH HDMI/DP,pcm=9"
P: Phys=ALSA
S: Sysfs=/devices/pci0000:00/0000:00:0e.0/sound/card0/input11
U: Uniq=
H: Handlers=event11
B: PROP=0
B: EV=21
B: SW=140

I: Bus=0000 Vendor=0000 Product=0000 Version=0000
N: Name="HDA Intel PCH HDMI/DP,pcm=10"
P: Phys=ALSA
S: Sysfs=/devices/pci0000:00/0000:00:0e.0/sound/card0/input12
U: Uniq=
H: Handlers=event12
B: PROP=0
B: EV=21
B: SW=140

I: Bus=0018 Vendor=04f3 Product=3157 Version=0100
N: Name="ASUE1409:00 04F3:3157 Mouse"
P: Phys=i2c-ASUE1409:00
S: Sysfs=/devices/pci0000:00/0000:00:17.1/i2c_designware.1/i2c-5/i2c-ASUE1409:00/0018:04F3:3157.0001/input/input16
U: Uniq=
H: Handlers=mouse0 event13
B: PROP=0
B: EV=17
B: KEY=30000 0 0 0 0
B: REL=1943
B: MSC=10

I: Bus=0018 Vendor=04f3 Product=3157 Version=0100
N: Name="ASUE1409:00 04F3:3157 Touchpad"
P: Phys=i2c-ASUE1409:00
S: Sysfs=/devices/pci0000:00/0000:00:17.1/i2c_designware.1/i2c-5/i2c-ASUE1409:00/0018:04F3:3157.0001/input/input17
U: Uniq=
H: Handlers=mouse1 event14
B: PROP=5
B: EV=1b
B: KEY=e520 10000 0 0 0 0
B: ABS=2e0800000000003
B: MSC=20

I: Bus=0018 Vendor=04f3 Product=3157 Version=0100
N: Name="ASUE1409:00 04F3:3157 Keyboard"
P: Phys=i2c-ASUE1409:00
S: Sysfs=/devices/pci0000:00/0000:00:17.1/i2c_designware.1/i2c-5/i2c-ASUE1409:00/0018:04F3:3157.0001/input/input18
U: Uniq=
H: Handlers=sysrq kbd event15 leds
B: PROP=0
B: EV=120013
B: KEY=1000000000007 ff800000000007ff febeffdfffefffff fffffffffffffffe
B: MSC=10
B: LED=1f

I: Bus=0003 Vendor=13d3 Product=5a11 Version=1702
N: Name="USB2.0 VGA UVC WebCam: USB2.0 V"
P: Phys=usb-0000:00:15.0-5/button
S: Sysfs=/devices/pci0000:00/0000:00:15.0/usb1/1-5/1-5:1.0/input/input42
U: Uniq=
H: Handlers=kbd event5
B: PROP=0
B: EV=3
B: KEY=100000 0 0 0

```
Look at the last entry. You can see that the Name field has a value of
```
N: Name="USB2.0 VGA UVC WebCam: USB2.0 V"
```
That's what you're looking for. Something with the word "webcam" in it.
From that entry, copy down the "Vendor=" and "Product=" values from the line above it. So mine are 13d3 and 5a11, respectively.

Now that you have those two numbers, go back to the command line and type:
```
foo@bar~$ cd /sys/bus/usb/devices
foo@bar~$ grep 13d3 */idVendor
```
and you will get a list of all devices on your system made by that vendor. Again, here is mine:
```
1-4/idVendor:13d3
1-5/idVendor:13d3
```
OK, so we've got two devices made by the same vendor (company). Now we narrow it down again to a single (hopefully) product. Type this in to the shell:
```
foo@bar~$ grep 5a11 */idProduct
```
and you should get only one result:
```
1-5/idProduct:5a11
```
As you can see, the numbers before the slash ("1-5") match one of the vendor entries, so your cam_id should be "1-5".

And here's how to find the KEY_WMI_* values for the keys you want to map:

Press the key you want to map a few times, then do this:
```
foo@bar~$ dmesg
```
where the you should find this in the output:
```
[30999.432449] asus_wmi: Unknown key 85 pressed
[31001.608410] asus_wmi: Unknown key 85 pressed
[31001.608410] asus_wmi: Unknown key 85 pressed
```

In this case scancode 85 is my camera key.
Note that these are hex values so the camera key becomes 133.

Use these values in Asus_L410M_WMI_Keys.py to fire events for your unused keys. Also if you have other keys that don't work, and you know python, you can map more keys to more functions.

# -)
