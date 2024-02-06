"""
The test_manager is responsible for the intake, execution, and output of all test
cases executed.
"""
import os
from pathlib import Path
from configparser import ConfigParser
from datetime import datetime, timedelta
from gui import popups
import logger as log
from communication.adb import Adb
from utilities.utilities import get_value_ini

# Paths to folders relative to this py file.
local_path = os.path.dirname(os.path.abspath(__file__))

# The paths to output the logging and the database file datas.
log_path = os.path.join(local_path, "app_log")

# Note: gui system logging is sent to a dedicated file due to track any issues with the external system at ease.
logger = log.make_logger(
    f_hdlr="rotate",
    save_path=log_path,
    log_prefix="test_logger",
    debug=1,
    logger_name="test_logger"
)

test_list = "settings\settings.ini"
test_path = os.path.join(local_path, test_list)

class TestManager:
    def __init__(self, mode, settings_lst):
        logger.debug(f"Initializing {__class__.__name__}")
        self.mode = mode
        self.settings_lst = settings_lst
        self.config = ConfigParser()
        self.config.read(test_path)
        self.reset_failure()

    def reset_failure(self):
        self.is_failure = False
        self.failure_name = None
        self.results = []
        
    def set_fail(self, is_fail, failure):
        self.is_failure = is_fail
        self.failure_name = failure
        
    def check_operator(self, operator, last_scan_time, timeout_minutes=30):
        current_time = datetime.now()

        if operator is None or (current_time - last_scan_time) > timedelta(minutes=timeout_minutes):
            operator = popups.serial('Numero de empleado:', 'Captura de empleado')
        return operator, current_time

    def system_start(self):
        reply_window = popups.image_yes_no('¿Se muestra esta pantalla?', get_value_ini(self.settings_lst, 'path_image_1'), 'Power_On')
        if reply_window == "Yes":
            result = "True"
            is_complete = True
        if reply_window == "No":
            result = "False"
            logger.debug("UUT no power On")
            self.set_fail(True, "system_start")
            # popups.ok('Unidad no enciendo, entregar a analisis', background_color= 'red')
            is_complete = False
        self.results.append(result)
        logger.debug("Run_Test: UUT no power On")
        return is_complete
    

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
                if self.is_failure:
                    logger.debug(f"Run_Test: Sequence is failure in {test_name} test")
                    break