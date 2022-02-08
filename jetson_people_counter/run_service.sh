#!/usr/bin/env bash

cd /home/master/workspace/python/jetson_people_counter
export DISPLAY=:0
xhost +
/usr/bin/python3 /home/master/workspace/python/jetson_people_counter/mipicam_tracking.py
