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
    
except ImportError as ie:
    logger.exception(f"An error occurred during initial import. Exiting.\n{ie}")
    sys.exit()
except Exception:
    logger.exception(f"An unknown Exception occurred when importing.")
    sys.exit()
logger.debug('Importing completed.')

settings_fname = "test_settings.ini"
config = ConfigParser()
config.read(os.path.join(app_path, 'settings', settings_fname))
settings_lst = [(s, dict(config.items(s))) for s in config.sections()]

def get_value(keyname):
    value = Kimball_Trace().get_value_ini(settings_lst, keyname)
    return value

def main():
    pups = popups
    kt = Kimball_Trace()
    
    while(True):
        try:
            # Ask the DUT serial to operador
            serial = pups.serial('Captura de serial')
            if serial == None:
                popups.quick_msg('Se esta cerrando la secuencia', display_sec= 5)
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
            
            result_turn_on = popups.image_yes_no('test', get_value('path_image_1'))
            if result_turn_on == 'No':
                popups.ok('Unidad no enciendo, entregar a analisis', background_color= 'red')
                continue

            popups.image_ok('Presione OK cuando la unidad muestre esta pantalla', get_value('path_image_2'))
            
        except Exception as e:
            logger.exception(f'The sequence is closing for exception, {e}')
            popups.quick_msg('Cerrando la secuencia por un error, revisar el logfile', display_sec= 5)
            sys.exit()

if __name__ == '__main__':
    main()