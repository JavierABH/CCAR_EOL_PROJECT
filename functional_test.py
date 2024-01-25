"""
Main application for performing functional test on CCAR EOL.
"""

# Force the CWD to be in this file directory.
import os

app_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(app_path)

# Make an application log output folder if not exists.
app_log_path = os.path.join(app_path, "app_log")
os.makedirs(app_log_path, exist_ok=True)

# Setup the application logger.
import logger as log

logger = log.make_logger(
    f_hdlr="rotate", save_path=app_log_path, log_prefix="funcional_log", debug=1
)
logger.debug("Logging is alive.")

# Trying importing other modules. End program if error.
try:
    import sys
    
    from gui import popups as pups
    
except ImportError as ie:
    logger.exception(f"An error occurred during initial import. Exiting.\n{ie}")
    sys.exit()
except Exception:
    logger.exception(f"An unknown Exception occurred when importing.")
    sys.exit()
logger.debug('Importing completed.')


def main():
    # pups.ok('ok')
    # pups.yes_no('yes_no')
    # pups.ok_cancel('ok_cancel')
    # pups.notify('notify')
    # pups.quick_msg('quick_msg')
    # print(sg.popup_get_text('text'))
    # pups.image_yes_no('The DUT is power on?', r'Pictures\5 Boot image.PNG')
    pups.serial()
    pass
    

if __name__ == '__main__':
    main()