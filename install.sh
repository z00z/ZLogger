#!/usr/bin/env bash

rm /var/lib/dpkg/lock
rm /var/cache/apt/archives/lock
rm /var/lib/apt/lists/lock
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y wine  
wget https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe
wine python-3.12.3-amd64.exe
sudo wine /root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python312/python.exe -m pip install pyinstaller pynput
sudo pip3 install pynput pyinstaller
