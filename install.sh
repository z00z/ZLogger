#!/usr/bin/env bash

rm /var/lib/dpkg/lock
rm /var/cache/apt/archives/lock
rm /var/lib/apt/lists/lock
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y wine python-pip 
wget https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi
wine msiexec /i python-2.7.14.msi
sudo wine ~/.wine/drive_c/Python27/python.exe -m pip install pyinstaller==3.6 pynput==1.6.8
sudo pip install pynput==1.6.8 pyinstaller==3.3.1
apt install -y gnome-shell-extension-dashtodock
