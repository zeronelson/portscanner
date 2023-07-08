import threading
import socket
import subprocess
import sys
import re
from datetime import datetime
from queue import Queue
import socket
import time

print_lock = threading.Lock()
target = 'hackthissite.org'

def scan(port):
    if port != 0:
        portscan(port)
        #banner()
        #checkport()
    else:
        #banner()
        portscan(port)

def portscan(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((target, port))
        sock.settimeout(0.1)
        sock.setblocking(1)
        with printLock:
            if result == 0:
                print(f"Port {port}:    Open")
            else:
                print(f"Port {port}:    Closed")
        sock.close()
    except:
        pass


# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()

        # Run the example job with the avail worker in queue (thread)
        scan(worker)

        # completed with the job
        q.task_done()



        

# Create the queue and threader 
q = Queue()

# how many threads are we going to allow for
for x in range(30):
     t = threading.Thread(target=threader)

     # classifying as a daemon, so they will die when the main dies
     t.daemon = True

     # begins, must come after daemon definition
     t.start()


start = time.time()

# 100 jobs assigned.
for worker in range(1,100):
    q.put(worker)

# wait until the thread terminates.
q.join()