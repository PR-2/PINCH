#!/bin/bash
sudo modprobe ftdi_sio && \
sudo sh -c  'echo "1b5c 0104" > /sys/bus/usb-serial/drivers/ftdi_sio/new_id' && \
sudo chmod 777 /dev/serial/by-id/usb-ICPDAS_I-7561U_USB_Serial_Converter_00Z5SFYW-if00-port0 && \
source activate py27 && \
(python server_capacity_changer.py & python ask_capacity_changer.py & python run.py &)