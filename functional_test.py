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
    from report.report import History
    from test_manager import TestManager
    from utilities.ping import scan_ip

except ImportError as ie:
    logger.exception(f"An error occurred during initial import. Exiting.\n{ie}")
    sys.exit()
except Exception:
    logger.exception(f"An unknown Exception occurred when importing.")
    sys.exit()
logger.debug('Importing completed.')

def main():
    kt = Kimball_Trace()
    logfile = History()
    settings_lst = kt.case_settings_lst
    
    test = TestManager(kt.mode, settings_lst)
    operator = None
    last_scan_time = None
    while(True):
        test.reset_failure()
        failstring = ""
        pass_fail = 1
        failure = ""
        
        try:
            operator, last_scan_time = test.check_operator(operator, last_scan_time)
            if operator in [None, '']:
                popups.ok('Numero de empleado no valido, vuelva a escanear', background_color= 'red')
                operator = None
                last_scan_time = None
                continue

            # Ask the DUT serial to operador
            serial = popups.serial('Serial:', 'Captura de serial')
            if serial == None:
                popups.quick_msg('Cerrando la secuencia', display_sec= 5)
                logger.info('Sequence is closing')
                break
            elif serial == "" or not kt.valid_serial(serial, 1):
                popups.ok('Serial no valido, vuelva a escanear', background_color= 'red')
                continue
                
            if not kt.valid_partnumber(serial):
                popups.ok('El numero de parte escaneado es incorrecto', background_color= 'red')
                continue
            
            if not kt.start_test():
                popups.ok(kt.reply_TracMex, background_color= 'red')
                continue
            # Init test
            while(True):
                if not test.system_start():
                    break
                
                list_ip = scan_ip()
                if len(list_ip) > 1:
                    popups.ok('Se ha detectado dos UUT encendidas\n'
                           'apague la que no esta usando', background_color= 'red')
                    break

            end_time = kt.get_date()
            
            logfile.add_results_to_logs(kt.part_number,
                                    kt.test_start_time,
                                    end_time,
                                    kt.trace_enable,
                                    test.is_failure,
                                    serial,
                                    test.results
                                    )
            
            if test.is_failure:
                pass_fail = 0
                failure = test.failure_name
                failstring = logfile.get_fail_string(failure)
                popups.ok(f'UUT fallo en {test.failure_name}', background_color= 'red')
            
            if not kt.send_result(pass_fail, failstring, operator):
                popups.ok(kt.replyInsert, background_color= 'red')
                
        except Exception as e:
            logger.exception(f'The sequence is closing for exception, {e}')
            popups.quick_msg('Cerrando la secuencia por un error, revisar funcional_log', display_sec= 5) 
            sys.exit()

if __name__ == '__main__':
    main()