from report.report import History
from datetime import datetime

date = datetime.now().strftime("%m-%d-%Y")
log = History()
log.add_results_to_logs('12EASDSAF1 + 1', date, date, False, False, 12323123, ["False", 'True'])
fail = log.get_fail_string('System_start')
print(fail)