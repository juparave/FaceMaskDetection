#!/usr/bin/bash

cd /home/pi/export_pi
export DISPLAY=:0
xhost +
/usr/bin/python3 /home/pi/export_pi/opencv_dnn_infer.py --img-mode 0 --video-path 0 > /home/pi/export_pi/run.log 2>&1
