import re
import os
import settings
import logparser
import reports

fd2 , temp_filename2 = reports.get_temp_file()

def get_log_regex():
    '''
     Appplication web server used to parse logs
    '''
    if settings.app_web_server == "apache" :
        reg_expression = settings.apache_regex
    elif settings.app_web_server == 'ngnix' :
        reg_expression = settings.ngnix_regex 
    return reg_expression

    
if __name__ == "__main__":
    '''
    Main method to handle logparser and sending reports
    '''
    files = []  #list of files to write log informations
    count_dict, temp_filename1, time = logparser.get_error_notification(settings.logpath, get_log_regex()) 
    reports.write_urls_count(fd2, count_dict)  
    content, subject = reports.report_generate(count_dict, time)
    files.append(temp_filename2)
    files.append(temp_filename1)
    reports.send_report(settings.recipient_email, content, subject, files)
    os.close(fd2)