"""
This module is for perform daily logfiles of DUTs
"""

import os
from pathlib import Path
from datetime import datetime
import csv
import logger as log

# Paths to folders relative to this py file.
local_path = os.path.dirname(os.path.abspath(__file__))
parent_path = Path(local_path).parent.absolute()

# The paths to output the logging and the database file datas.
log_path = os.path.join(parent_path, "app_log")

# Note: historical system logging is sent to a dedicated file due to track
# any issues with the external system at ease.
logger = log.make_logger(
    f_hdlr="rotate",
    save_path=log_path,
    log_prefix="logfiles_logger",
    debug=1,
    logger_name="DUT_logger"
)

testname_fname = "testnames.txt"
testname_path = os.path.join(parent_path, 'settings', testname_fname)
logfiles_dir = os.path.join(local_path, 'logfiles')

class History:
    def __init__(self):
        """
        Initialize the History class and create a log file if it doesn't exist.

        Returns:
            None
        """
        try:
            logger.debug(f"Initializing {__class__.__name__}")
            self._create_log()
        except Exception as e:
            logger.exception(f"An error occurred when initializing History: {e}")
    
    def _generate_logfile_name(self):
        """
        Generates the name for the logfile based on the current date.

        Returns:
            str: The generated logfile name.
        """
        today = datetime.now().strftime("%m-%d-%Y")
        return f"CCAR_EOL_{today}.csv"
    
    def _generate_logfile_path(self):
        """
        Generates the full path for the logfile.

        Returns:
            str: The generated logfile path.
        """
        try:
            self.logfile_name = self._generate_logfile_name()
            self.logfile_path = os.path.join(logfiles_dir, self.logfile_name)
            return self.logfile_path
        except Exception as e:
            logger.exception(f"Error generating logfile path: {e}")

    def _create_log(self):
        """
        Creates a new log file if it doesn't exist.

        Returns:
            None
        """
        info_columns = ["Date", "PartNumber", "StartTime", 
         "EndTime", "TraceEnable", "TestResult", "SerialNumber"]
        try:
            self.logfile_path = self._generate_logfile_path()
            if not os.path.exists(self.logfile_path):
                with open(self.logfile_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    header = self._get_header()
                    writer.writerows(header)
                    final_row = info_columns + [""] * (len(header[0]) - 7)
                    writer.writerow(final_row)
                logger.debug(f"New logfile was created: {self.logfile_name}")
        except Exception as e:
            logger.exception(f"Error creating log file: {e}")
    
    def _get_column_data(self, column):
        """
        Retrieves data from a specific column in the testname file.

        Args:
            column (int): The index of the column to retrieve.

        Returns:
            list: A list containing the data from the specified column.

        Exception:
            Exception: If an error occurs while reading or processing the testname file.
        """
        try:
            with open(testname_path, 'r') as file:
                column_data = [line.strip().split(',')[column] for line in file]
            return column_data
        except Exception as e:
            logger.exception(f"Error getting column data: {e}")
            return []

    def _get_header(self):
        """
        Retrieves header data from different columns in the testname file.

        Returns:
            list: A list containing rows of testnames, low_limits, high_limits,
                  expected_values, units, and logic_operators.

        Exception:
            Exception: If an error occurs while reading or processing the testname file.
        """
        try:
            blanks = [""] * 6
            testnames = blanks + self._get_column_data(0)
            low_limits = blanks + self._get_column_data(1)
            high_limits = blanks + self._get_column_data(2)
            expected_values = blanks + self._get_column_data(3)
            units = blanks + self._get_column_data(4)
            logic_operators = blanks + self._get_column_data(5)
            test_rows = [
                testnames,
                low_limits,
                high_limits,
                expected_values,
                units,
                logic_operators]
            return test_rows
        except Exception as e:
            logger.exception(f"Error getting header data: {e}")
            return []
    
    def add_results_to_logs(self, PartNumber, StartTime, EndTime, TraceEnable,
                            TestResult, SerialNumber, result_data):
        """
        Adds the provided result data to the log file.

        Args:
            PartNumber (str): The DUT part number.
            StartTime (str): The start time of the test.
            EndTime (str): The end time of the test.
            TraceEnable (str): Indicator of traceability enablement.
            TestResult (str): The result of the test.
            SerialNumber (str): The DUT serial number.
            result_data (list): List of results of the test.

        Returns:
            None
        """
        Date = datetime.now().strftime("%H:%M:%S")
        try:
            self._create_log()
            expected_length_tests = len(self._get_header()[0]) - 7
            
            result_data = result_data + [""] * (expected_length_tests - len(result_data))
            data = [Date, PartNumber, StartTime, EndTime, 
                    TraceEnable, TestResult, SerialNumber] + result_data
            
            with open(self.logfile_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)
                
            logger.debug(f"add data to serial:{result_data[0]}")
        except Exception as e:
            logger.exception(f"Error adding results to logs: {e}")
    
    def _get_rows(self, path):
        """
        Reads and returns the rows from a file.

        Args:
            path (str): The path to the file.

        Returns:
            list: A list containing the rows read from the file.

        Raises:
            Exception: If an error occurs while reading the file.
        """
        try:
            loglines = []
            with open(path) as file:
                for line in file.readlines():
                    loglines.append(line.rstrip())
            return loglines
        except Exception as e:
            logger.exception(f"Error getting rows: {e}")
            return []
        
    def _get_columns_byname(self, path, column):
        """
        Retrieves data from a specific column in a CSV file using column names.

        Args:
            path (str): The path to the CSV file.
            column (str): The name of the column to retrieve.

        Returns:
            list: A list containing the data from the specified column.

        Raises:
            Exception: If an error occurs while reading or processing the CSV file.
        """
        try:
            with open(path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                column_data = [row[column] for row in reader]
            return column_data
        except Exception as e:
            logger.exception(f"Error getting columns by name: {e}")
            return []
        
    def get_fail_string(self, testname):
        """
        Retrieves failure information for a specific testname.

        Args:
            testname (str): The testname to search for.

        Returns:
            str: A formatted string containing failure information.

        Raises:
            Exception: If an error occurs while processing the testname file or log file.
        """
        try:
            lines = self._get_rows(testname_path)
            for line in lines:
                if testname in line:
                    low_limit = line.split(',')[1]
                    high_limit = line.split(',')[2]
                    expect_value = line.split(',')[3]
                    unit = line.split(',')[4]
                    logic_operator = line.split(',')[5]

            column_data = self._get_columns_byname(self.logfile_path, testname)
            test_measurement = column_data[-1]
            fail_string = f"|ftestres=0,{testname},{test_measurement},{high_limit},{low_limit},{expect_value},{unit},{logic_operator}"
            return fail_string
        except Exception as e:
            logger.exception(f"Error getting fail string: {e}")
            return ""