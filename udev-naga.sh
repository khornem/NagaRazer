#!/bin/bash

export DISPLAY=:0
export XAUTHORITY=/home/miguel/.Xauthority
/usr/bin/python /usr/local/bin/naga_razer.py
notify-send "test naga"
