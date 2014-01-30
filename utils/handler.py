import re
import os
import sys
import settings
import logparser
import reports
import time, sys
from boto.s3.connection import S3Connection


fd2 , temp_filename2 = reports.get_temp_file()

def get__aws_logs(env_id):
    '''
    Get amozon aws logs from simple storage Service data storage and save it to given path
    '''
    conn = S3Connection()
    bucket = conn.get_bucket('elasticbeanstalk-us-east-1-660104689325')
    keys = bucket.list(prefix='resources/environments/logs/publish/' + env_id) 
    for key in keys:
        key_name = str(key.key)
        key.last_modified
        filename = key_name.split('/')[-1]
        path = '/home/arya/Desktop/log/' + filename 
        if '_access_log'  in filename : 
            key.get_contents_to_filename(path)

def get_log_regex(server):
    '''
     Appplication web server used to parse logs
    '''
    if server == "apache" :
        reg_expression = settings.apache_regex
    elif server == 'ngnix' :
        reg_expression = settings.ngnix_regex 
    return reg_expression


def handle(*args, **options):
    env_name = args[0][0]
    env_id = args[0][1]
    path =  args[0][2]
    server = args[0][3]  
    mailTo = args[0][4]
    get__aws_logs(env_id) 
    count_dict, temp_filename1, time = logparser.get_error_notification(path, get_log_regex(server))
    return count_dict, temp_filename1, time , mailTo, env_name ,env_id

if __name__ == "__main__":
    '''
    Main method to handle logparser and sending reports
    ''' 
    files = []
    if len(sys.argv) == 1:
         #list of files to write log informations
        get__aws_logs(settings.env_id)
        count_dict, temp_filename1, time = logparser.get_error_notification(settings.logpath, get_log_regex(settings.app_web_server)) 
        reports.write_urls_count(fd2, count_dict)  
        content, subject = reports.report_generate(count_dict, time)
        files.append(temp_filename2)
        files.append(temp_filename1)
        reports.send_report(settings.recipient_email, content, subject, files, settings.project)
        os.close(fd2)
    else: 
        count_dict, temp_filename1, time , mailTo, env_name ,env_id= handle(sys.argv[1:])
        reports.write_urls_count(fd2, count_dict)  
        content, subject = reports.report_generate(count_dict, time)
        files.append(temp_filename2)
        files.append(temp_filename1)
        reports.send_report(mailTo, content, subject, files, env_name)
        os.close(fd2)
    
        