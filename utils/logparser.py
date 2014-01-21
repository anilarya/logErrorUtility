import re
import os
import datetime
import sys 
import fnmatch
import gzip  
import io
import reports
import settings


def lines_from_dir(filepat, dirname):
    names =  find_files(filepat,dirname)
    files =  open_files(names)
    lines =  concatenate(files)
    return lines

def find_files( filepat,top):
    '''A function that generates files that match a given filename pattern'''
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist,filepat):
            yield os.path.join(path,name)

def open_files( filenames):
    for name in filenames:
        if name.endswith(".gz"):
            yield gzip.open(name)
#        elif name.endswith(".bz2"):
#            yield bz2.BZ2File(name)
        else:
            yield open(name)

def concatenate( sources):
    '''Concatenate multiple generators into a single sequence'''
    for s in sources:
        for item in s:
            yield item


def grep(pat,lines):
    '''A function that generates lines that match a given pattern'''
    patc = re.compile(pat)
    for line in lines:
        if patc.search(line): yield line

def get_log_re():
    if settings.app_server == "apache" :
        reg_expression = settings.apache_regex
    elif settings.app_server == 'ngnix' :
        reg_expression = settings.ngnix_regex
    log_re = re.compile(reg_expression)
    return log_re

def get_error_notification(recipient_email, path):
    ''' A function to parse logs  and return count_dictionary of log errors '''
    wwwlog = lines_from_dir('*.log1',path)
    count_dict = reports.get_count_dict() 
    fd, temp_filename = reports.get_temp_file()
    c = 0
    log_re = get_log_re()
    for line in wwwlog : 
        c = c + 1
        m = log_re.match(line)
        if m : 
            request = m.groupdict()
            if c == 1:
                time = request["request"].split(":")[0]
            count_dict, fd = reports.get_count_information(count_dict, fd, request) 
    os.close(fd)    
    if c == 0 : 
        print "No logs found" 
        return
    content,subject = reports.report_generate(count_dict, time)
    reports.send_report(recipient_email, content, subject, temp_filename)

    
if __name__ == "__main__":
    if settings.mode == "local": 
        get_error_notification(settings.recipient_email, settings.path)
    else : 
        pass