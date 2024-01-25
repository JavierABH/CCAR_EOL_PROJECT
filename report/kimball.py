"""
This module is for Kimball Traceability system
"""

import sys
sys.path.append(r'C:\CCAR_EOL_Project')

import os
import clr
from configparser import ConfigParser
from pathlib import Path
import logger as log
from exceptions import TraceabilityError, BarcodeError

# Paths to folders relative to this py file.
local_path = os.path.dirname(os.path.abspath(__file__))
parent_path = Path(local_path).parent.absolute()

# The paths to output the logging and the database file datas.
log_path = os.path.join(parent_path, "app_log")

# Note: Traceability system logging is sent to a dedicated file due to track any issues with the external system at ease.
logger = log.make_logger(
    f_hdlr="rotate",
    save_path=log_path,
    log_prefix="trace_log",
    debug=1,
    logger_name="traceability_logger"
)

class Kimball_Trace:
    def __init__(self, dut_name):
        try:
            logger.debug(f"Initializing {__class__.__name__}")
            settings_fname = "settings.ini"
            config = ConfigParser()
            config.read(os.path.join(local_path, settings_fname))
            
            # Make a list of the settings to reference for TODO IMEI and ICCID
            self.case_settings_lst = [(s, dict(config.items(s))) for s in config.sections()]
            
            self.wsconnector_path = config["PATHS"]["wsconnector_path"]
            self.newtonsoftjson_path = config["PATHS"]["newtonsoftjson_path"]
            
            # Lowercase the status in case of user input error.
            self.trace_enable = (config["OPTIONS"]["trace_enable"]).lower()
            self.record_fail = (config["OPTIONS"]["record_fail"]).lower()
            self.part_number = config[dut_name.upper()]["part_number"]
            
            self.process_name = config["STATION"]["process_name"]
            self.station_name = config["STATION"]["station_name"]
            
            clr.AddReference(self.newtonsoftjson_path)
            clr.AddReference(self.wsconnector_path)
            
            from WSConnector import Connector

            self.connector = Connector()
            
        # Execute except block if module error occurs.
        except ModuleNotFoundError:
            logger.exception("An exception was raised in making the instance of traceability system.")
        except TraceabilityError:
            logger.exception("An exception was raised in making the instance of the Traceability system.")
            raise
        except Exception:
            logger.exception("An error occurred when making connection with Traceability system.")
            raise
            
    def is_valid_serial(self, serial_number , serial_length = ):
        pass
    
    def start_test(self):
        pass
    
    def send_result(self):
        pass