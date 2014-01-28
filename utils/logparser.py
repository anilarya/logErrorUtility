import re
import os
import datetime
import sys 
import fnmatch
import gzip  
import io
import reports
import settings
from urlparse import urlsplit, parse_qsl
import dateutil.parser 
from collections import Counter
import operator
import pandas as pd
import numpy as np
from pandas import Series, DataFrame, Panel


unique_set = Counter()

def lines_from_dir(filepat, dirname):
    '''
    Read lines from given directory
    '''
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

def get_sorted_values(urls_count_dict):
    sorted_dict = sorted(urls_count_dict.iteritems(), key=operator.itemgetter(1), reverse =True)
    return sorted_dict
    
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

def _parse_query_parameters(url):
    query_string = urlsplit(url)[3]
    params = parse_qsl(query_string, 
                               keep_blank_values=True, strict_parsing=False)
    prefixed_params = map(lambda kv: ("qs_%s" % kv[0], kv[1]), params)
    return dict(prefixed_params)

def _get_path(url):
    return urlsplit(url)[2]


def _coerce_float(maybe_float):
    try:
        return float(maybe_float.strip())
    except:
        return float('nan')

def _coerce_int(maybe_int):
    try:
        return int(maybe_int.strip())
    except:
        return -1

def _pretty_url(url):
    if not url:
        return None
    tokens = url.split("/")
#     print tokens
    if tokens[1] in ('v1', 'v2', 'v3'):
        return tokens[2]
    else:
        return tokens[1]

def ip_requests(log_list, count_dict) :
    '''
    Pandas applications
    '''
    df = DataFrame(log_list)
    ips = df.groupby('clientip').size()
    ips.sort()
    ips_fd = DataFrame({'Number of requests':ips[-10:]})
    ips_fd = ips_fd.sort(columns='Number of requests',  ascending=False)
    count_dict['ips_fd'] = ips_fd
    return count_dict

def slower_than(cutoff, request):
    request['response_time'] = _coerce_float(request['response_time'])
    if request['response_time'] > cutoff: 
         yield request

def slow_urls_and_their_counts(request):
    '''
    Calculate slower URLS having response time >=2.0 ms
    '''
    logs = slower_than(2.0, request)  # Change  cutoff accordingly as per the requirements
    for log in logs:
        unique_set[log['url']] += 1
    unique_dict = {}
    for url, count in unique_set.items():
        unique_dict[url]  = count 
    return  unique_dict 

def get_general_loginfo(request, count_dict,  log_list, fd):
    log_list.append(request)
    time = request["request"].split(" ")[0].split("[")[1] 
    time = datetime.datetime.strptime(str(time), '%d/%b/%Y:%H:%M:%S')
    count_dict = reports.get_count_information(count_dict, fd, request)
    urls_count_dict = slow_urls_and_their_counts(request)
    count_dict  = ip_requests(log_list, count_dict)   #Data analysis using python pandas
    return count_dict , urls_count_dict , time

def parse(wwwlog, regex, count_dict, fd):
    '''
    Utility to parse logs and return errors_count dictionary
    '''
    log_list = []
    log_re = re.compile(regex)
    for line in wwwlog:
        m = log_re.match(line) 
        if not m:
            continue
        request =  m.groupdict()
        count_dict, urls_count_dict , time = get_general_loginfo(request, count_dict, log_list, fd)
    count_dict["slow_urls_count"] = get_sorted_values(urls_count_dict)
    return count_dict, time


def get_error_notification(path, regex):
    ''' A function to parse logs  and return count_dictionary of log errors 
    '''
    wwwlog = lines_from_dir('*.log1',path)
    count_dict = reports.get_count_dict()
    time = datetime.datetime.now()
    fd, temp_filename = reports.get_temp_file() 
    count_dict, time= parse(wwwlog, regex, count_dict, fd)
    os.close(fd)
    return count_dict, temp_filename, time

if __name__=="__main__":
    pass