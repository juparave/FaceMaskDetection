# OpenCV DNN Infer

Install requirements

    $ pip install -r requirements.txt

sudo apt-get install python3-rpi.gpio

run command:

    $ python3 opencv_dnn_infer.py --img-mode 0 --video-path 0

## service configuration

`export_pi/run_service.sh`

    #!/usr/bin/bash
    cd /home/pi/export_pi
    /usr/bin/python3 /home/pi/export_pi/opencv_dnn_infer.py --img-mode 0 --video-path 0 > /home/pi/export_pi/run.log 2>&1

`/lib/systemd/system/face_detector.service`

    [Unit]
    Description=Detector Service
    After=multi-user.target
    
    [Service]
    Type=idle
    
    WorkingDirectory=/home/pi/export_pi
    ExecStart=/home/pi/export_pi/run_service.sh
    
    Restart=always
    [Install]
    WantedBy=multi-user.target


Then set 644 permissions on the unit file:

    $ sudo chmod 644 /lib/systemd/system/face_detector.service

Enable service at boot

    $ sudo systemctl daemon-reload
    $ sudo systemctl enable sample.service