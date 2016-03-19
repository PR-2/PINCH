import os
import signal
import subprocess

p = subprocess.Popen(['ps', '-au'], stdout=subprocess.PIPE)
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
    stop(line, "ask_power.py")
    stop(line, "server_capacity_changer.py")
    stop(line, "ask_capacity_changer")
