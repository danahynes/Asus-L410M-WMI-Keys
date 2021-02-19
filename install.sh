#! /bin/bash
#------------------------------------------------------------------------------#
# Filename: install.sh                                           /          \  #
# Project : Asus_L410M_WMI_Keys                                 |     ()     | #
# Date    : 02/17/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# copy files to location
sudo cp ./asus_l410m_wmi_keys.py /usr/bin
sudo cp ./asus_l410m_wmi_keys.service /lib/systemd/system/

# start service now and on reboot
sudo systemctl start asus_l410m_wmi_keys
sudo systemctl enable asus_l410m_wmi_keys

# -)
