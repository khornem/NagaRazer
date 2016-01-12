#!/bin/bash


if [[ $(whoami) != "root" ]];
then
    echo "Error: execute with sudo"
    exit 0
fi

if [[ $# != 1 ]];
    then
    echo "Usage: sudo ./install.sh <user>"
    exit 0
fi

echo "--- installing python-dev, needed for evdev package"
apt-get install python-dev
echo "--- installing evdev"
pip install evdev
echo "--- installing xdotool, needed for implement actions"
apt-get install xdotool
echo "--- installing udev developer library"
apt-get install libudev-dev
echo "--- installint python uinput"
pip install python-uinput

echo "--- Creating naga_razer.py in /usr/local/bin for user $1"
sed "s/miguel/$1/g" ./naga_razer.py > /usr/local/bin/naga_razer.py

echo "--- Creating config in $HOME/.config/NagaRazer"
mkdir $HOME/.config/NagaRazer

echo "--- Creating initial sample configuration file"
sed "s/miguel/$1/g" ./naga_config.json > $HOME/.config/NagaRazer/naga_config.json

echo "--- Copying udev rule"
cp ./40-mouse-razer.rules /etc/udev/rules.d/

echo "--- Creating udev script"
sed "s/miguel/$1/g" ./udev-naga.sh > /usr/local/bin/udev-naga.sh

echo "--- Copying configurator script"
cp ./NagaConfigurator.py /usr/local/bin/ 