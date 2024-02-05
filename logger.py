"""
Logger is responsible for create a logfile and saves the register actions modules
"""

import logging
from logging.handlers import RotatingFileHandler
from os.path import join as join

def make_logger(f_hdlr="file", log_prefix="", save_path=".", _datetime=None, **kwargs):
    """
    Create a new file and streaming logger.

    Debug mode is initially set True when first generated.
    Default logger name is "application_logger".

    Args:
        f_hdlr (str, optional): The file handler type as FileHandler or RotatingFileHandler. Defaults to "file". ["file", "rotate"]
        log_prefix (str, optional): The name to append to the front of all log files. Defaults to "".
        save_path (str, optional): The absolute path to save log files to. Defaults to ".".
        _datetime (str, optional): The datetime to add to log filename. Used only with file handler type. Defaults to None.

    Returns:
        logging.logger: A logging object with streaming and file handlers.
    """
    try:
        # Create logger.
        logger_name = kwargs.get("logger_name", "application_logger")
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # Console and file handlers.
        ch = logging.StreamHandler()

        # Setup single file handler or rotating handler to 25MB cap and 20 files.
        if f_hdlr.lower().startswith("rotate"):
            f_name = f"{log_prefix}.log"
            fh = RotatingFileHandler(
                filename=join(save_path, f_name), maxBytes=25_000_000, backupCount=10
            )
        else:
            f_name = f"{log_prefix}_{_datetime}.log"
            fh = logging.FileHandler(filename=join(save_path, f_name))

        ch.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)

        # Console and file formatters.
        c_formatter = logging.Formatter("%(message)s")
        f_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
        )

        # Add formatters to ch.
        ch.setFormatter(c_formatter)
        fh.setFormatter(f_formatter)

        # Add ch to logger.
        logger.addHandler(ch)
        logger.addHandler(fh)

        return logger
    except Exception:
        raise


def set_debug(logger, lvl):
    """
    Set the logging level of the logger between INFO and DEBUG.

    Args:
        logger (logging.logger): A logging object instance.
        lvl (bool): True or False to enable or disable debug mode respectively.
    """
    try:
        if lvl:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        logger.debug(f"Logging debug set to: {lvl}")
    except Exception as e:
        logger.error(f"An Exception occurred when setting logging debug level: {e}")
