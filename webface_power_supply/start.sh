#!/bin/bash
sudo modprobe ftdi_sio && \
sudo sh -c  'echo "1b5c 0104" > /sys/bus/usb-serial/drivers/ftdi_sio/new_id' && \
sudo chmod 777 /dev/ttyUSB1 && \
sudo chmod 777 /dev/ttyUSB2 && \
source activate py27 && \
(python server_ps_3_2_1_3000_dc.py & python ask_ps_3_2_1_3000_dc.py & python run.py &)