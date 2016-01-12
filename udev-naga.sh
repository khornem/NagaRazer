#!/bin/bash


if [[ $(pgrep -c udev-naga.sh) -gt 1 ]]
then
   exit 0
fi

export DISPLAY=:0
export XAUTHORITY=/home/miguel/.Xauthority
/usr/bin/python /usr/local/bin/naga_razer.py
notify-send "test naga"
