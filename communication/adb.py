import os
import subprocess
import re
import logging

logger = logging.getLogger("funcional_log")

class Adb():
    def __init__(self):
        logger.debug(f"Initializing {__class__.__name__}.")
        self.path = r"C:\scrcpy"
        self.ip = None
    
    def start_server(self):
        """
        Starts the ADB server
        """
        command = ["adb", "start-server"]

        p = subprocess.Popen(command, stderr=None, stdout=None)
        p.wait(timeout=10)
        print("ADB server has been started.")
        
    def kill_server(self):
        """
        Kills the ADB server
        """
        command = ["adb", "kill-server"]

        p = subprocess.Popen(command, stdout=None, stderr=None)
        p.wait(timeout=10)
        print("ADB server has been killed.")
        
    def connect_device(self, ip):
        pass
    
    def run_command(self, arg_string, arg_list):
        """
        Run a general ABD command
        """
        command = arg_list if arg_list else str(arg_string).split(" ")

        p = subprocess.check_output(command, stderr=None)
        print(p.decode('utf-8'))
        
adb = Adb()
adb.start_server()
adb.kill_server()