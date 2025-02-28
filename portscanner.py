"""
This is a simple port scanner that scans a given target on a given
range of ports and checks if they are open or not. It uses threads
to speed up the process. The results are stored in a list.
"""

import socket
import threading
from queue import Queue

target = "127.0.0.1"

# queue to store all ports
queue = Queue()
# list to store open ports
open_ports = []

# function to check if a port is open
def portscan(port):
    try:
        # try to connect to the port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except: 
        # if connection fails, port is not open
        return False

"""
# sequential port scanning
for port in range(1, 1024):
    result = portscan(port)
    if result:
        print("Port {} is open".format(port))
    else:
        print("Port {} is closed".format(port))
"""

#using threads and queue
# function to fill the queue with port numbers
def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

# worker function for each thread
def worker():
    while not queue.empty():
        port = queue.get()
        # check if port is open
        if portscan(port):
            print("Port {} is open".format(port))
            # add port to list of open ports
            open_ports.append(port)

# generate a list of ports to check
port_list = range (1, 65000)
fill_queue(port_list)

# create a list to store all threads
thread_list = []

# create 100 threads
for t in range(100):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

# start all threads
for thread in thread_list:
    thread.start()

# wait for all threads to finish
for thread in thread_list:
    thread.join()

print("Open Ports :", open_ports)
