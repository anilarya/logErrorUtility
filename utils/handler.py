import re
import settings
import logparser
import reports

def get_log_regex():
    if settings.app_web_server == "apache" :
        reg_expression = settings.apache_regex
    elif settings.app_web_server == 'ngnix' :
        reg_expression = settings.ngnix_regex 
    return reg_expression

if __name__ == "__main__":
    count_dict, fd, filename, time = logparser.get_error_notification(settings.logpath, get_log_regex())
    content, subject = reports.report_generate(count_dict, time)
    reports.send_report(settings.recipient_email, content, subject, filename)