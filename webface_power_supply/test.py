import gevent
def wait():
    while True:
        print("In loop")
        gevent.sleep(1) # To not fill the screen..
g = gevent.spawn(wait)
print g
g.join(timeout=5)
