#!/bin/bash
sudo modprobe ftdi_sio && \
sudo sh -c  'echo "1b5c 0104" > /sys/bus/usb-serial/drivers/ftdi_sio/new_id' && \
sudo chmod 777 /dev/ttyUSB0 && \
source activate py27 && \
(python capacity_server.py & python ask_capacity_changer.py & python run.py &)