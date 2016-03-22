import gevent

from connection import connect_to_server

while True:

    command_list = ['IReg_C1-value', 'IReg_C2-value', 'IReg_C-value',
                     'IReg_Amplitude-mismatch', 'IReg_Phase-mismatch']
    #command_list = ['IReg_Amplitude-mismatch', 'IReg_Phase-mismatch']
    for command in command_list:
        msg = command + " = "

        datagram = connect_to_server("/tmp/python_unix_sockets_capacity", None, msg)

        gevent.sleep(1)
