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
    from gui import popups
    from report.kimball import Kimball_Trace
    from configparser import ConfigParser
    from utilities.utilities import get_value_ini
    from test_manager import TestManager
    
except ImportError as ie:
    logger.exception(f"An error occurred during initial import. Exiting.\n{ie}")
    sys.exit()
except Exception:
    logger.exception(f"An unknown Exception occurred when importing.")
    sys.exit()
logger.debug('Importing completed.')

def main():
    pups = popups
    kt = Kimball_Trace()
    test = TestManager(kt.mode)

    settings_lst = kt.case_settings_lst
    
    while(True):
        try:
            # Ask the DUT serial to operador
            serial = pups.serial('Captura de serial')
            if serial == None:
                popups.quick_msg('Cerrando la secuencia', display_sec= 5)
                logger.debug('Sequence is closing')
                break
            elif serial == "" or not kt.valid_serial(serial):
                popups.ok('Serial no valido, vuelva a escanear', background_color= 'red')
                continue
            
            if not kt.valid_partnumber(serial):
                popups.ok('El numero de parte escaneado es incorrecto', background_color= 'red')
                continue
            
            if not kt.start_test():
                popups.ok(kt.reply_TracMex, background_color= 'red')
                continue
            
            while(True):
                result_turn_on = popups.image_yes_no('test', get_value_ini(settings_lst, 'path_image_1'))
                if result_turn_on == 'No':
                    popups.ok('Unidad no enciendo, entregar a analisis', background_color= 'red')
                    test_fail = 'power_on'
                    test_data = 'False'
                    break

                popups.image_ok('Presione OK cuando la unidad muestre esta pantalla', get_value_ini(settings_lst, 'path_image_2'))
            
        except Exception as e:
            logger.exception(f'The sequence is closing for exception, {e}')
            popups.quick_msg('Cerrando la secuencia por un error, revisar el logfile funcional_log.log', display_sec= 5) 
        finally:
            sys.exit()

if __name__ == '__main__':
    main()