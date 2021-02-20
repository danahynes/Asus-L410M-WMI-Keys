<!----------------------------------------------------------------------------->
<!-- Filename: README.md                                       /          \  -->
<!-- Project : Asus_L410M_WMI_Keys                            |     ()     | -->
<!-- Date    : 02/17/2019                                     |            | -->
<!-- Author  : Dana Hynes                                     |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# Asus_L410M_WMI_Keys

This small program runs at boot and gives you access to the keys on the keyboard that aren't handled by the current asus-nb-wmi driver.

On my laptop (a 2020 Asus L410M) these are the camera toggle key (same as F10) and the "Launch MyAsus" key (same as F12).

I banged my head against a wall for a few hours until I found a solution to this. At first I thought the asus-nb-wmi driver was swallowing events for keys it did not recognize (actually some programs, like xev, could see them being pressed and released but they just had 0x0 scancodes). But then I realized the asus-nb-wmi driver was logging them in dmesg as "unknown" keys, but with unique scancodes. Turns out that the python library libevdev can read the scancodes from the keyboard before the asus-nb-wmi driver throws them away.

For the camera key, I am "poking" a value into a file that the camera watches to see if it should be enabled.

Note that this is NOT a one-to-one hardware switch for the webcam. It will turn the webcam off if you're using an app that is using the webcam, but it won't turn back on if the app is still running. Also if you use the key while the camera is in use, there is an issue where the system file gets out of sync (I believe the app has a lock on the file) and you may have to press the button a few times with all apps closed to re-sync it. Also, there is no indicator for whether the cam is currently on or off. I'm working on these issues, but for now, "it mostly works™".

Also note that if no camera is found, or if more than one camera is found, the camera key will be remapped to Shift-Meta-R.

As for the "MyAsus" key, it presents itself as Shift-Meta-T. You should be able to map it to something useful using your system's keyboard shortcuts. I'm currently using it to launch Chromium and it works perfectly.

If the WMI keyboard can't be found, then all hope is lost and the programs quits.

# Installing

To install, clone the git repo:
```
foo@bar:~$ cd ~/Downloads
foo@bar:~$ git clone https://github.com/danahynes/Asus_L410M_WMI_Keys
foo@bar:~$ cd Asus_L410M_WMI_Keys
```

You MAY need to find the key scancodes and edit asus_l410m_wmi_keys.py before you install.

**See note below!**

Once you do that, you can install by:
```
foo@bar:~$ sudo ./install.sh
```
You can also download the [latest release](http://github.com/danahynes/Asus_L410M_WMI_Keys/releases), unzip it, set the scancodes in asus_l410m_wmi_keys.py, and run the install.sh file from there.

# Uninstalling

To uninstall, go to the git directory and run:
```
foo@bar:~$ sudo ./uninstall.sh
```

# Finding the KEY_WMI_* values

Here's how to find the KEY_WMI_* values for the keys you want to map:

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
Note that these are hex values so the camera key 0x85 becomes 133 decimal.

Use these values in asus_l410m_wmi_keys.py to fire events for your unused keys. Also if you have other keys that don't work, and you know python, you can map more keys to more functions if you have other non-working keys.

# TODO

1. a LOT more checks to see if files exist
1. more error checking
1. camera file lock checking/syncing
1. camera status indicator

# -)
