import os
import signal
import subprocess

p = subprocess.Popen(['ps', '-aux'], stdout=subprocess.PIPE)
out, err = p.communicate()


def stop(process, name):
    if name in process.lower():
        pid = int(process.split()[1])
        print process.lower()
        print pid
        os.kill(pid, signal.SIGKILL)


for line in out.splitlines():
    stop(line, "server.py")
    stop(line, "run.py")
    stop(line, "server_gauge.py")
    stop(line, "ask_gauge.py")
    stop(line, "server_rrg.py")
    stop(line, "ask_rrg.py")
    stop(line, "ask_power.py")
    stop(line, "server_capacity_changer.py")
    stop(line, "ask_capacity_changer.py")
    stop(line, "server_ps_3_2_1_3000_dc.py")
    stop(line, "ask_ps_3_2_1_3000_dc.py")
    stop(line, "ask_cito.py")
    stop(line, "server_cito_1330.py")

