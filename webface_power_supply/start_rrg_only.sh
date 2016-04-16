#!/bin/bash
sudo modprobe ftdi_sio && \
sudo sh -c  'echo "1b5c 0104" > /sys/bus/usb-serial/drivers/ftdi_sio/new_id' && \
sudo chmod 777 /dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0 && \
source activate py27 && \
(python server_rrg.py & python ask_rrg.py & python run.py &)