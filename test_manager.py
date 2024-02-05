"""
The test_manager is responsible for the intake, execution, and output of all test
cases executed.
"""
import os
import logging
from configparser import ConfigParser

logger = logging.getLogger("test_logger")
local_path = os.path.dirname(os.path.abspath(__file__))
test_list = "settings\settings.ini"
test_path = os.path.join(local_path, test_list)

class TestManager:
    def __init__(self, mode):
        logger.debug(f"Initializing {__class__.__name__}")
        self.mode = mode
        self.config = ConfigParser()
        self.config.read(test_path)  # Lee el archivo de configuración
        
    def run_mode(self):
        try:
            # Check if the user has entered the wrong settings in 'OPTIONS' of settings.ini
            pass
        except:
            pass

    def system_start(self):
        if self.mode == 'manual':
            pass

    def wifi(self):
        print("Ejecutando WiFi")

    def lte_modem_configuration(self):
        print("Ejecutando LTE_modem_configuration")

    def download_v4app(self):
        print("Ejecutando Download_V4APP")

    def vdu_config(self):
        print("Ejecutando VDU_config")

    def run_tests(self):
        test_sequence = self.config.get('TestSequence', 'sequence').split(',')
        for test_name in test_sequence:
            test_method_name = test_name.strip()
            if hasattr(self, test_method_name):
                getattr(self, test_method_name)()
            else:
                print(f"Método {test_method_name} no encontrado")
