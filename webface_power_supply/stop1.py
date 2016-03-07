import os
import signal
import subprocess

p = subprocess.Popen(['ps', 'au'], stdout=subprocess.PIPE)
out, err = p.communicate()


def stop(process, name):
    if name in process.lower():
        pid = int(process.split()[1])
        print process.lower()
        print pid
        os.kill(pid, signal.SIGKILL)


for line in out.splitlines():
    # print line
    stop(line, "server.py")
    stop(line, "run.py")
