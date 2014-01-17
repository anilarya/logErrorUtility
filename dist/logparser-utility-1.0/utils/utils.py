'''
Created on 8th Jan 2014
@author: Anil Arya 
'''

import re
import os
import smtplib 
import datetime
import sys 
import fnmatch
import gzip 
from email.mime.text import MIMEText
from collections import defaultdict 
from fabric.api import * 
import template


SMTP_CONF = {
             "MAIL_ENABLE": False,
             "MAIL_RECIPIENTS_OVERRIDE": False,
             "MOCK_MAIL_RECIPIENTS": [],
             "SERVER":"smtp.gmail.com",
             "PORT":587,
             "USERNAME":"wspalerts@hmadev.com",
             "PASSWORD":"w5p4l3rt5"
             }
             
def handle(*args, **options):
    start_timestamp = args[0][0] 
    end_timestamp = args[0][1]
    path =  args[0][2] 
    recipient_email = args[0][3]
    get_error_notification(start_timestamp, end_timestamp,  recipient_email, path) 

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


def send_email(fromaddress,toaddresses,content,subject = "" ): 
    me = fromaddress
    you = toaddresses
    smtp_server = SMTP_CONF["SERVER"]
    smtp_username = SMTP_CONF["USERNAME"]
    smtp_password = SMTP_CONF["PASSWORD"]
    smtp_port = SMTP_CONF["PORT"] 
    msg = MIMEText(content, 'html', _charset='utf-8')
    msg['Subject'] ='["Status Report]: %s'% ( subject)
    msg['From'] = me        
    msg['To'] =  you     
    reciepents = toaddresses.split(',') 
    server = smtplib.SMTP(smtp_server,smtp_port, local_hostname='wspalerts@hmadev.com') 
    server.starttls()
    server.login(smtp_username,smtp_password) 
    server.sendmail(fromaddress,reciepents,msg.as_string())
    server.quit()
    return True

def get_email_html_body(start_timestamp, end_timestamp, count):  
    a =  getattr(template,'email_content_for_error_count' )
    email_body = a()%(start_timestamp, end_timestamp, count['total']['total_Count'], count["4xx"][ "4xx_Counts"],\
              count["5xx"][ "5xx_Counts"], count["2xx"][ "2xx_Counts"]) 
    return email_body


def get_timestamp(timestamp):
    month_dict = {
              '01':"Jan",'02':"Feb" , '03':"Mar" , '04': "Apr" , '05' :"May" , '06' : "Jun",\
                '07': "Jul" ,'08': "Aug", '09' : "Sep", '10':"Oct" ,  '11':"Nov"  , '12':"Dec"  }
    
    time_token =  str(timestamp.split('T')[1])
    date_token =  timestamp.split('T')[0]
    year = str(date_token.split('-')[0])
    date = str(date_token.split('-')[1])
    month = str(date_token.split('-')[2]) 
    res_timestamp = date + "/" + month_dict[month] + "/" +  year + ":" + time_token  
    return  res_timestamp 

def get_count_information(count, request):
    if  request['status'] >='500' and request['status'] < '600':
        count["5xx"]['5xx_Counts'] += 1 
    elif  request['status'] >='400'and request['status'] < '500':
        count["4xx"]['4xx_Counts'] += 1  
    elif  request['status'] >='200' and request['status'] < '300' :
        count["2xx"]['2xx_Counts'] += 1
        
    count['total']['total_Count'] += 1
    return count

def get_count_dict() : 
    count = {
                 "4xx" :
                 {
                   "4xx_Counts":0
                 },
                 "5xx" :
                 {
                  "5xx_Counts" : 0
                 },
                 "2xx" :
                 {
                  "2xx_Counts" : 0 
                 },
                 "total":
                 {
                   "total_Count" :0
                 }
             
         }
    return count
def get_error_notification(st_timestamp, en_timestamp, recipient_email, path):
    start_timestamp = get_timestamp(st_timestamp)  
    end_timestamp = get_timestamp(en_timestamp) 
    wwwlog = lines_from_dir('*.log',path)  
    log_re = re.compile('^(?P<timestamp>\d+/\w+/\d+\:\d+\:\d+\:\d+) (?P<status>\d+) (?P<response_time>[\d.-]+)')
    start_timestamp = datetime.datetime.strptime(str(start_timestamp), '%d/%b/%Y:%H:%M:%S')
    end_timestamp = datetime.datetime.strptime(str(end_timestamp), '%d/%b/%Y:%H:%M:%S') 
    count_dict = get_count_dict () 
    c = 0
    for line in wwwlog :
        c = c + 1 
        m = log_re.match(line)  
        if m : 
            request = m.groupdict() 
            time = request["timestamp"]
            time = datetime.datetime.strptime(str(time), '%d/%b/%Y:%H:%M:%S')  
            if time >= start_timestamp and  time <= end_timestamp : 
                count_dict = get_count_information(count_dict, request)
         
    if c == 0 : 
        print "No logs found" 
        return 
    fromaddress = SMTP_CONF["USERNAME"]
    valid_recipents_address =  recipient_email
    if count_dict['4xx']["4xx_Counts"] != 0 or count_dict['5xx']["5xx_Counts"] != 0:
        subject = " ::  %d Messages Failed" %(count_dict['5xx']["5xx_Counts"] +  count_dict['4xx']["4xx_Counts"])
        content = get_email_html_body(start_timestamp, end_timestamp,count_dict)
    elif count_dict['4xx']["4xx_Counts"] == 0 and count_dict['5xx']["5xx_Counts"] == 0 :
        subject = ":: No errors during:  %s -- %s" %(start_timestamp , end_timestamp) 
        content = ""  
        print "No Error found"
            
    send_email(fromaddress,valid_recipents_address, content,subject) 

if __name__ == "__main__":
    handle(sys.argv[1:])
