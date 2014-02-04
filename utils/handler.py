import re
import os
import sys
import settings
import datetime
import logparser
import reports
import time, sys
from boto.s3.connection import S3Connection


fd2 , temp_filename2 = reports.get_temp_file()

def get_aws_logs(env_id, bucket_name, prefix_key, log_path):
    '''
    Get amozon aws logs from simple storage Service data storage and save it to given path
    '''
    conn = S3Connection()
    bucket = conn.get_bucket(bucket_name)
    keys = bucket.list(prefix= prefix_key + env_id) 
    for key in keys:
        key_name = str(key.key)
        date = logparser.yester_date
        today = datetime.datetime.now()
        yester_date = date.strftime('%Y-%m-%d') 
        today = today.strftime('%Y-%m-%d') 
        filename = key_name.split('/')[-1]
        path = log_path + filename  
        if ('_access_log'  in filename) and ((key.last_modified.split('T')[0] == yester_date)\
                                        or(key.last_modified.split('T')[0] == today.split(' ')[0]) ):
            key.get_contents_to_filename(path)

def get_log_regex(regex_type):
    '''
     Appplication web server used to parse logs
    '''
    if regex_type == "apache" :
        reg_expression = settings.apache_regex
    elif regex_type == 'ngnix' :
        reg_expression = settings.ngnix_regex 
    return reg_expression


def handle(*args, **options): 
    '''
    Command to run this utility :  
    python /home/arya/apps/logErrorUtility/utils/handler.py  <env-Name> <env-Id> <bucket-Name> <Prefix-key> <log-path>\
        <regex-server>  <recipients_emailId>
    '''
    env_name = args[0][0]
    env_id = args[0][1]
    bucket_name = args[0][2]
    prefix_key = args[0][3]
    path =  args[0][4]
    regex_type = args[0][5]  # regex_type :  like apache or ngnix
    mailTo = args[0][6]
    
    get_aws_logs(env_id, bucket_name, prefix_key, path) 
    count_dict, temp_filename1, time = logparser.get_error_notification(path, get_log_regex(regex_type))
    return count_dict, temp_filename1, time , mailTo, env_name

if __name__ == "__main__":
    '''
    Main method to handle logparser and sending reports
    ''' 
    files = []
    if len(sys.argv) == 1:
        '''
        configuration from settings.py : Used for extension of usage as Application
        '''
         #list of files to write log informations
#        get_aws_logs(settings.env_id)
#        count_dict, temp_filename1, time = logparser.get_error_notification(settings.logpath, get_log_regex(settings.app_web_server)) 
#        reports.write_urls_count(fd2, count_dict)  
#        content, subject = reports.report_generate(count_dict, time)
#        files.append(temp_filename2)
#        files.append(temp_filename1)
#        reports.send_report(settings.recipient_email, content, subject, files, settings.project)
#        os.close(fd2)
    else: 
        '''
        if len(sys.argv) > 1 :  if length of arguments is greater than one.
        configuration from  commandline Arguments
        ''' 
        count_dict, temp_filename1, time , mailTo, env_name = handle(sys.argv[1:]) 
        reports.write_urls_count(fd2, count_dict)  
        content, subject = reports.report_generate(count_dict, time)
        files.append(temp_filename2)
        files.append(temp_filename1)
        reports.send_report(mailTo, content, subject, files, env_name)
        os.close(fd2)