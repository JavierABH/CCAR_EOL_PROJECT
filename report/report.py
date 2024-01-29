"""
This module is for perform daily logfiles
"""

import os
from pathlib import Path
import logger as log

# Paths to folders relative to this py file.
local_path = os.path.dirname(os.path.abspath(__file__))
parent_path = Path(local_path).parent.absolute()

# The paths to output the logging and the database file datas.
log_path = os.path.join(parent_path, "app_log")

# Note: gui system logging is sent to a dedicated file due to track any issues with the external system at ease.
logger = log.make_logger(
    f_hdlr="rotate",
    save_path=log_path,
    log_prefix="logfiles_logger",
    debug=1,
    logger_name="DUT_logger"
)

testname_fname = "testnames.txt"
