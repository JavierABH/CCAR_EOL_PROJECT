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
        self._create_log()
    
    def _generate_logfile_name(self):
        today = datetime.now().strftime("%m-%d-%Y")
        return f"CCAR_EOL_{today}.csv"
    
    def _generate_logfile_path(self):
        self.logfile_name = self._generate_logfile_name()
        self.logfile_path = os.path.join(logfiles_dir, self.logfile_name)
        return self.logfile_path

    def _create_log(self):
        self.logfile_path = self._generate_logfile_path()
        if not os.path.exists(self.logfile_path):
            with open(self.logfile_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                header = self._get_header()
                writer.writerows(header)
                serial_row = ["Serial"] + [""] * (len(header[0]) - 1)
                writer.writerow(serial_row)
    
    def _get_column_data(self, column):
        with open(testname_path, 'r') as file:
            column_data = [line.strip().split(',')[column] for line in file]
        return column_data

    def _get_header(self):
        testnames = self._get_column_data(0)
        low_limits = self._get_column_data(1)
        high_limits = self._get_column_data(2)
        expected_values = self._get_column_data(3)
        units = self._get_column_data(4)
        logic_operators = self._get_column_data(5)
        rows = [
            testnames,
            low_limits,
            high_limits,
            expected_values,
            units,
            logic_operators]
        return rows
    
    def add_results_to_logs(self, result_data):
        self._create_log()
        header = self._get_header()
        expected_length = len(header[0])
        result_data = result_data + [""] * (expected_length - len(result_data))
        with open(self.logfile_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(result_data)
    
    def _get_files(self, path):
        loglines = []
        with open(path) as file:
            for line in file.readlines():
                loglines.append(line.rstrip())
            return loglines
        
    def _get_columns_byname(self, path, column):
        with open(path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            column_data = [row[column] for row in reader]
        return column_data
        
    def get_fail_string(self, testname):
        lines = self._get_files(testname_path)
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