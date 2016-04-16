#!/bin/bash
sudo modprobe ftdi_sio && \
sudo sh -c  'echo "1b5c 0104" > /sys/bus/usb-serial/drivers/ftdi_sio/new_id' && \
if [ ! -f /dev/serial/by-id/usb-ICPDAS_I-7561U_USB_Serial_Converter_00Z5SFYW-if00-port0 ]; then
    sudo chmod 777 /dev/serial/by-id/usb-ICPDAS_I-7561U_USB_Serial_Converter_00Z5SFYW-if00-port0
    echo "ICPDAS_I-7561U_USB_Serial_Converter_00Z5SFYW exist"
fi
if [ ! -f /dev/serial/by-id/usb-ICPDAS_I-7561U_USB_Serial_Converter_00Z5PSMV-if00-port0 ]; then
    sudo chmod 777 /dev/serial/by-id/usb-ICPDAS_I-7561U_USB_Serial_Converter_00Z5PSMV-if00-port0
    echo "ICPDAS_I-7561U_USB_Serial_Converter_00Z5PSMV exist"
fi

source activate py27 && \
(python server_ps_3_2_1_3000_dc.py & python ask_ps_3_2_1_3000_dc.py & python run.py &)