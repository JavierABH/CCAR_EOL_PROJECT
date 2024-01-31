"""
Ping module for scanning a range of IP addresses concurrently.
"""
from threading import Thread
import subprocess
import queue
import re

# some global vars
num_threads = 20
ips_q = queue.Queue()
out_q = queue.Queue()

# CCIVisage AP Kimball has ip range of 192.168.17.101 to 192.168.17.250
kimball_ip = "192.168.17." 
# build IP array
ips = []
for i in range(101,250):
    ips.append(kimball_ip+str(i))
    
# thread code : wraps system ping command
def thread_pinger(i, q):
    """
    Pings hosts in the queue.

    Args:
        i (int): Thread index.
        q (Queue): Queue containing IP addresses to ping.
        
    Returns:
        None
    """
    while True:
        # get an IP item form queue
        ip = q.get()
        # ping it
        args = ["PING.EXE", "-n", "1", "-w", "1", str(ip)]
        p_ping = subprocess.Popen(args,
                                  shell=False,
                                  stdout=subprocess.PIPE)
        # save ping stdout
        p_ping_out = str(p_ping.communicate()[0])
        
        if p_ping.wait() == 0:
            # Minimum = 1ms, Maximum = 1ms, Average = 1ms
            search = re.search(
                "Minimum = (.*)ms, Maximum = (.*)ms, Average = (.*)ms",
                p_ping_out,
                re.M | re.I,
            )
            ping_rtt = search.group(3)
            out_q.put(str(ip))
            
        # update queue : this ip is processed
        q.task_done()

def scan_ip():
    """
    Scans a range of IP addresses concurrently using threading.
    
    Returns:
        list: A list of IP addresses that responded to the ping.
    """
    # start the thread pool
    for i in range(num_threads):
        worker = Thread(target=thread_pinger, args=(i, ips_q))
        worker.setDaemon(True)
        worker.start()
    
    # fill queue
    for ip in ips:
        ips_q.put(ip)
        
    # wait until worker threads are done to exit
    ips_q.join()
    ip_list = []
    while True:
        try:
            ip = out_q.get_nowait()
            ip_list.append(ip)
        except queue.Empty:
            break
    return ip_list