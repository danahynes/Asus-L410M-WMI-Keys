#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: install.sh                                           /          \  #
# Project : Asus_L410M_WMI_Keys                                 |     ()     | #
# Date    : 02/17/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# NB: doesn't matter if run as sudo or not

# show some progress
# NB: first call with sudo to ask for password on its own line (aesthetics)
sudo echo "Installing Asus_L410M_WMI_Keys... "
echo "For license info see the LICENSE.txt file in this directory"

# install dependencies
sudo echo "Installing dpendencies... "
sudo apt-get install python3-libevdev
echo "Done"

# copy files to location
echo -n "Copying files... "
sudo cp ./asus_l410m_wmi_keys.py /usr/bin
sudo cp ./asus_l410m_wmi_keys.service /lib/systemd/system/
echo "Done"

# start service now and on reboot
echo "Starting service... "
sudo systemctl start asus_l410m_wmi_keys
sudo systemctl enable asus_l410m_wmi_keys
echo "Done"

# -)
