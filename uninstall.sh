#!/usr/bin/env bash
#------------------------------------------------------------------------------#
# Filename: uninstall.sh                                         /          \  #
# Project : Asus_L410M_WMI_Keys                                 |     ()     | #
# Date    : 02/17/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

# stop service now and on reboot
sudo systemctl stop asus_l410m_wmi_keys
sudo systemctl disable asus_l410m_wmi_keys

# delete files from location
sudo rm /usr/bin/asus_l410m_wmi_keys.py
sudo rm /lib/systemd/system/asus_l410m_wmi_keys.service

# -)
