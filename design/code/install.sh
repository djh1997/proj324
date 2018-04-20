#!/bin/sh

sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus python-pip python-imaging python-numpy
sudo pip install python-telegram-bot --upgrade
sudo pip install RPi.GPIO
sudo pip install Adafruit_GPIO
pip install -U scikit-image
mkdir setup
cd setup||return '54'
wget https://github.com/cskau/Python_ST7735/archive/master.zip
unzip master.zip
cd master||return '55'
sudo python setup.py install
curl -s -L https://remote-iot.com/install/remote-iot-install.sh | sudo -s bash
sudo /etc/remote-iot/services/setup.sh
curl -s -L https://remote-iot.com/install/upgrade.sh | sudo -s bash
