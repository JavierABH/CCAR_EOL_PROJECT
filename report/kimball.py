"""
This module is for Kimball Traceability system
"""

import os
import clr
from configparser import ConfigParser
from pathlib import Path
from datetime import datetime
import logger as log
from exceptions import TraceabilityError

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
    def __init__(self):
        try:
            logger.debug(f"Initializing {__class__.__name__}")
            settings_fname = "settings.ini"
            config = ConfigParser()
            config.read(os.path.join(local_path, settings_fname))
            
            # Make a list of the settings to reference for TODO IMEI and ICCID
            self.case_settings_lst = [(s, dict(config.items(s))) for s in config.sections()]
            
            self.wsconnector_path = config["PATHS"]["wsconnector_path"]
            self.newtonsoftjson_path = config["PATHS"]["newtonsoftjson_path"]
            
            # Settings to be used
            self.is_status_set = False
            self.can_testing = False
            
            # Lowercase the status in case of user input error.
            self.trace_enable = (config["OPTIONS"]["trace_enable"]).lower()
            self.part_number = config["TRIDENT_DISPLAY"]["part_number"]
            self.process_name = config["STATION"]["process_name"]
            self.station_name = config["STATION"]["station_name"]
            
            # If the Traceability is desactivated in settings, no actions associated with the system will be executed.
            if not self.is_traceability_enable():
                logger.debug(f'The traceability system is disabled.')
                return None
            
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

    def valid_serial(self, serial_number , length = 30):
        """
        Verifies if the serial number passed on is of the correct length

        Args:
            serial_number (String) - The serial number on the DUT.
            length (int, optional): Set the length of the serial number on the DUT. Defaults to 30.

        Returns:
            Boolean: The result of whether the method was executed successfully.
        """        
        try:
            if not self.is_traceability_enable():
                logger.debug(f'The traceability system is disabled. No serial validation is performed')
                return True
            
            serial_number_length = len(serial_number)
            if serial_number_length == length:
                return True
            else:
                logger.debug(f'the serial number {serial_number} does not have the required characters: {length}')
                return False
        except Exception:
            logger.exception("An error occurred when valid serial .")
            raise

    def valid_partnumber(self, serial_number):
        """
        Verifies if the serial number passed on is of the correct part number i.e. of the right DUT.

        Parameter:
                serial_number (String) - The serial number on the DUT.

        Returns:
                (Boolean) - The result of whether the method was executed successfully. 

        Exception:
                An exception arises when there is an error in the serial number scanned.
        """       
        reply_part_number, _ = " ", " "
        try:

            # If the Traceability is deactivated in settings, no actions associated with the system will be executed.
            if not self.is_traceability_enable():
                logger.debug(f'The traceability system is disabled. No part number validation is performed')
                return True

            self.serial_number = serial_number

            # Part number is tracked with the serial number
            reply_part_number, _ =  self.connector.CIMP_PartNumberRef(self.serial_number, 1, _)

            if reply_part_number == '' or reply_part_number == 'One or more errors occurred.':
                raise TraceabilityError('Connection error to the Traceability system.')
            elif not reply_part_number == self.part_number:
                logger.debug("The serial number scanned is incorrect DUT.")
                return False
            else:
                logger.debug("The serial number scanned is of the correct DUT.")
                return True

        except TraceabilityError:
            logger.exception("An exception was raised in verifying scanned serial number.")
            raise          
        except Exception:
            logger.exception("An exception was raised in verifying scanned serial number.")
            raise

    def start_test(self):
        """
        Checks if the DUT is undergoing the correct process and then, collects the start time of test.

        Parameter:
                None

        Returns:
                (Boolean) - The result of whether the method was executed successfully. 

        Exception:
                An exception arises when there is a mismatch between the 
        """
        self.reply_TracMex = None
        self.test_start_time = None
        self.test_end_time = None   
        try:
            # Request the start time (initial).
            self.test_start_time = self.get_date()
            # If the Traceability is deactivated in settings, no actions associated with the system will be executed.
            if not self.is_traceability_enable():
                logger.debug(f'The traceability system is disabled. Backcheck not perfomed.')
                return True

            replyBackCheck = self.connector.BackCheck_Serial(self.serial_number, self.station_name)
            logger.debug(f"Serial: {self.serial_number}, bk: {replyBackCheck}")
            status = replyBackCheck.split('|')[0]
            self.reply_TracMex = replyBackCheck.split('|')[1]
            
            if self.reply_TracMex == 'One or more errors occurred.':
                raise TraceabilityError(f"An Error ocurred as process name does not match: {replyBackCheck}.")
            
            if not status == 1:
                self.reply_TracMex = self.reply_TracMex.split('.')[0]
                return False
            
            return True

        except TraceabilityError:
            logger.exception("An exception was raised when starting the tests in the Traceability system.")
            raise
        except Exception:
            logger.exception("An error occurred when indicating starting of tests in the traceability system.")
            raise
    
    def send_result(self, test_result, fail_string, employee):
        """
        At the end of the test, takes the result and sends the test information to the Traceability system.

        Parameter:
                test_result (Int) - The result (0 is "FAIL, 1 is "OK") of the test.
                failure_string (String) - The response of the test in case of failure.
                employee (String) - The number employee performing the test.

        Returns:
                (Boolean) - The result of whether the method was executed successfully. 

        Exception:
                An exception arises when there is an issue with inserting a record to the database.
        """       
        try:
            # The time when test has ended is collected
            self.test_end_time = self.get_date()
            # If the Traceability is deactivated in settings, no actions associated with the system will be executed.
            if not self.is_traceability_enable():
                logger.debug(f'The traceability system is disabled. InsertProcess not perfomed.')
                return True
            
            # The test result with the details of the test setup is sent to the Traceability system.
            self.replyInsert = self.connector.InsertProcessDataWithFails(
                self.serial_number, 
                self.station_name, 
                self.process_name,
                self.test_start_time,
                self.test_end_time, 
                test_result, 
                fail_string, 
                employee)

            # If the insertion of the record occurs 
            if "Ok El serial fue insertado" in self.replyInsert or "OK | Insertado Correctamente" in self.replyInsert:
                logger.debug(f"Serial {self.serial_number}: {self.process_name} was passed successfully.")
                return True
            else:
                raise TraceabilityError(f"An Error ocurred as the traceability failed to upload: {self.replyInsert}")

        except TraceabilityError:
            logger.exception("An exception was raised when ending the tests in the Traceability system.")
            raise    

        except (RuntimeError, Exception):
            logger.exception("An error occurred when indicating ending of tests in the traceability system.")
            return False
    
    def get_value_ini(self, info, keyname):
        """
        Get the value associated with a specific keyname from the provided info.

        Parameters:
            info (list): List of tuples containing key-value pairs.
            keyname (str): The key to search for in the dictionaries within the tuples.

        Returns:
            The value associated with the specified keyname. Returns None if the key is not found.

        Exceptions:
            An exception is raised if an error occurs while searching for the keyname in the info list.
        """
        try:
            for tupla in info:
                if keyname in tupla[1]:
                    return tupla[1][keyname]
            return None
        except Exception:
            logger.exception("An error occurred when get key types of upload data in the traceability system.")
            raise
    
    def send_info_alternate(self, serial_alternate, type_alt, keyname):
        """
        Sends alternate information to the Traceability system.

        Parameters:
            serial_alternate (str): The alternate serial number.
            type_alt (int): The type of alternate information.
            keyname (str): The keyname to retrieve the type_alt value from the case settings list.

        Returns:
            True if the method was executed successfully.

        Exceptions:
            An exception is raised if an error occurs during the execution of the method.
        """
        type_alt = int(self.get_value_ini(self.case_settings_lst, keyname))
        
        try:
            # If the Traceability is deactivated in settings, no actions associated with the system will be executed.
            if not self.is_traceability_enable():
                logger.debug(f'The traceability system is disabled. InsertProcess not perfomed.')
                return True
            reply_insert_alt = self.connector.Insert_SN_Alternate(self.serial_number, serial_alternate, type_alt, self.station_name)
            if not reply_insert_alt == 'OK':
                raise TraceabilityError(f"An error ocurred as the traceability failed to upload {keyname}: {reply_insert_alt}")
            
            return True
            
        except TraceabilityError:
            logger.exception("An exception was raised when ending the tests in the Traceability system.")
            raise
        except Exception:
            logger.exception("An error occurred when indicating ending of tests in the traceability system.")
            raise
    
    def is_traceability_enable(self):
        '''
        The indicator for the traceability system indicates whether the system is enable or disabled.

        Parameter:
                None

        Returns:
                (Boolean) - The result being the status of the system: True or False.

        Exception:
                An exception arises when there is an issue with returning the status.
        '''
        try:
            # Check if the user has entered the wrong settings in 'OPTIONS' of settings.ini
            if not self.is_status_set:
                if self.trace_enable not in ['on', 'off']:
                    raise TraceabilityError(f"An error ocurred as the traceability's status is unrecognized : {self.trace_enable}.")
            
            # When Status is not set, the status is parsed from the settings.ini
            # and converted to either 'Connected' or 'Disabled'.
            if not self.is_status_set:
                
                if self.trace_enable == 'on':
                    self.trace_enable = True
                elif self.trace_enable == 'off':
                    self.trace_enable = False
                    
                self.is_status_set = True
                
            return self.trace_enable
        except (TraceabilityError,Exception):
            logger.debug("An exception was raised when the status of traceability integration is checked.")
            raise
        
    def get_date(self):
        """
        Gets the current datetime from the traceability system or the local system.

        Returns:
            str: The current datetime.
        """
        if self.is_traceability_enable():
            str_date = self.connector.CIMP_GetDateTimeStr()
        else:
            str_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return str_date