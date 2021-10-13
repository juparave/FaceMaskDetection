#!/usr/bin/bash

cd /home/pi/people_counter
export DISPLAY=:0
xhost +
/usr/bin/python3 /home/pi/people_counter/run.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt --model mobilenet_ssd/MobileNetSSD_deploy.caffemodel > /home/pi/people_counter/run.log 2>&1
