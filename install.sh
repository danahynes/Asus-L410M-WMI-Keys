#! /bin/bash
#------------------------------------------------------------------------------#
# Filename: install.sh                                           /          \  #
# Project : Asus_L410M_WMI_Keys                                 |     ()     | #
# Date    : 02/17/2021                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
#------------------------------------------------------------------------------#

sudo cp ./Asus_L410M_WMI_Keys.py /usr/bin
sudo cp ./Asus_L410M_WMI_Keys.service /lib/systemd/system/
sudo systemctl start Asus_L410M_WMI_Keys
sudo systemctl enable Asus_L410M_WMI_Keys

# -)
