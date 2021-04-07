<!----------------------------------------------------------------------------->
<!-- Filename: README.md                                       /          \  -->
<!-- Project : Asus_L410M_WMI_Keys                            |     ()     | -->
<!-- Date    : 02/17/2019                                     |            | -->
<!-- Author  : Dana Hynes                                     |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# Asus_L410M_WMI_Keys
## "It mostly works™"

This small program runs at boot and gives you access to the keys on the keyboard
that aren't handled by the current asus-nb-wmi driver.

On my laptop (a 2021 Asus L410M) these are the camera toggle key (same as *F10*)
and the "Launch MyAsus" or "//]" key (same as *F12*).

![](keys.jpg)

# Installing

To install, clone the git repo:
```bash
foo@bar:~$ cd ~/Downloads
foo@bar:~/Downloads$ git clone https://github.com/danahynes/Asus_L410M_WMI_Keys
foo@bar:~/Downloads$ cd Asus_L410M_WMI_Keys
```

You *may* need to find the key scancodes and edit *asus_l410m_wmi_keys.py*
before you install.

**See note below!**

Once you do that, you can install by:
```bash
foo@bar:~/Downloads/Asus_L410M_WMI_Keys$ ./install.sh
```
You can also download the
[latest release](http://github.com/danahynes/Asus_L410M_WMI_Keys/releases/latest),
unzip it, possibly set the scancodes in *asus_l410m_wmi_keys.py*, and run the
install.sh file as *sudo* from there.

# Uninstalling

To uninstall, go to the git directory and run:
```bash
foo@bar:~/Downloads/Asus_L410M_WMI_Keys$ ./uninstall.sh
```

or delete the files manually:
```bash
foo@bar:~$ sudo systemctl stop asus_l410m_wmi_keys
foo@bar:~$ sudo systemctl disable asus_l410m_wmi_keys
foo@bar:~$ sudo rm -rf /usr/bin/asus_l410m_wmi_keys.py
foo@bar:~$ sudo rm -rf /lib/systemd/system/asus_l410m_wmi_keys.service
foo@bar:~$ sudo rm -rf /var/log//asus_l410m_wmi_keys.log
```

# Finding the scancode values

Here's how to find the scancode values for the keys you want to map:

Press the key you want to map a few times, then do this:
```bash
foo@bar:~$ dmesg | grep "asus_wmi"
```
where you should find this near the end of the output:
```bash
[30999.432449] asus_wmi: Unknown key 85 pressed
[31001.608410] asus_wmi: Unknown key 85 pressed
[31001.608410] asus_wmi: Unknown key 85 pressed
```

In this case scancode 85 is my camera key. Note that this is a hex value so it
must be written as 0x85.

Use these values in *asus_l410m_wmi_keys.py* to fire events for your unused
keys. Find the section labeled with a comment of "THIS IS WHERE YOU ADD/EDIT
UNMAPPED KEYS" and add a constant:
```bash
KEY_WMI_<SOMENAME> = 0x<SCANCODE>
```

and add an array in the format:

```python3
key_wmi_<somename> = [
  KEY_WMI_<SOMENAME>,
  libevdev.EV_KEY.<KEY_CONSTANT>,
  ...
]

...

keys_wmi = [
  key_wmi_<somename>,
  ...
]
```

Replace the parts in <> with your values. Key constants can be found
[here](https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h).

You can also use *evtest* to find the scancodes but using dmesg is a little
faster and easier IMHO, so I won't explain it here.

# Notes

I banged my head against a wall for a few hours until I found a solution to
this. At first I thought the  
asus-nb-wmi driver was swallowing events for keys
it did not recognize (actually some programs, like *xev*, could see them being
pressed and released but they just had 0x0 scancodes). But then I realized the
asus-nb-wmi driver was logging them in *dmesg* as "unknown" keys, but with
unique scancodes. (I did later find out they were being recognized in evtest).
Turns out that the python library libevdev can read the scancodes from the
keyboard before the asus-nb-wmi driver throws them away!

Turning the camera on and off is still a work in progress, so for now the
"Toggle Camera" (*F10*) key is mapped to *Shift-Meta-R*. As for the "MyAsus"
key (*F12*), it presents itself as *Shift-Meta-T*. The screenshot (*F11*) key
is already mapped to *Shift-Meta-S*, so these seemed like reasonable values for
the keys to the left and right of it.

If the WMI keyboard can't be found, then all hope is lost and the programs
quits.

If it doesn't seem to be working right, check the log file:
``` bash
foo@bar:~$ cat /var/log/asus_l410m_wmi_keys.log
```

These keys are also function keys, so what happens when you press them
depends on the state of the *Fn* key. This laptop, and others like it, have a
"Function Lock" feature (similar to "Caps Lock") that is activated by pressing
*Fn+Esc*. This feature is set to "on" at boot, so you may need to turn it off
or press *Fn* along with the key to get the desired behavior. The
"Function Lock" feature can be turned off in the BIOS menu, in which case you
need to press the *Fn* key with the desired key to use the WMI function (volume,
  screen brightness, etc.), otherwise pressing the key alone sends *Fn(N)*.

Also note that this will **not** allow you to remap keys that are already
handled by the asus-nb-wmi driver. It may be possible but this program does not
and will not attempt to do it.

# TODO

1. enable/disable camera on the fly (i.e. without reboot or restart app)
1. camera file lock checking/syncing
1. camera enabled indicator (not the same as the in-use light)

# -)
