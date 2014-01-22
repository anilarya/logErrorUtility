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

def get_error_notification(path, regex):
    ''' A function to parse logs  and return count_dictionary of log errors '''
    wwwlog = lines_from_dir('*.log',path)
    count_dict = reports.get_count_dict() 
    fd, temp_filename = reports.get_temp_file()
    log_re = re.compile(regex)
    time=None 
    for line in wwwlog : 
        m = log_re.match(line)
        if m : 
            request = m.groupdict()
            time = request["request"].split(":")[0]
            count_dict, fd = reports.get_count_information(count_dict, fd, request) 
    os.close(fd)
    return count_dict, fd , temp_filename , time

#if __name__=="__main__":
#    path = args[0]
#    regex = args[1]
#    get_error_notification(path, regex)