from report.report import History

log = History()
# log.add_results_to_logs(['21301230023', 'True', 'fail', 'test'])
fail = log.get_fail_string('power_on')