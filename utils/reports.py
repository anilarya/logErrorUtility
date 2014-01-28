import os
import render
import mail , settings
import tempfile
import operator

def get_temp_file():
    fd, filename = tempfile.mkstemp() 
    return fd, filename
    
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

def get_count_information(count, fd, request):
    if  request['status'] >='500' and request['status'] < '600':
        os.write(fd, str(request))
        os.write(fd, '\n\n')
        count["5xx"]['5xx_Counts'] += 1 
    elif  request['status'] >='400'and request['status'] < '500':
        count["4xx"]['4xx_Counts'] += 1  
    elif  request['status'] >='200' and request['status'] < '300' :
        count["2xx"]['2xx_Counts'] += 1
    count['total']['total_Count'] += 1
    return count

def write_urls_count(fd2, count_dict):
    os.write(fd2, '=============================Slow urls with number of Hits===============================\n\n')
    for urls in count_dict["slow_urls_count"]:
        os.write(fd2, str(urls))
        os.write(fd2,'\n')
    os.write(fd2, "\n======================clientIps and Number of requests made by same Ips==================\n\n")
    os.write(fd2, str(count_dict["ips_fd"]))

def report_generate(count_dict, start_timestamp):
    if count_dict['4xx']["4xx_Counts"] != 0 or count_dict['5xx']["5xx_Counts"] != 0:
        subject = "[Daily Status Report]:::  %d Messages Failed" %(count_dict['5xx']["5xx_Counts"] +  count_dict['4xx']["4xx_Counts"])
        content = render.get_email_html_body(start_timestamp, count_dict)
    elif count_dict['4xx']["4xx_Counts"] == 0 and count_dict['5xx']["5xx_Counts"] == 0 :
        subject = "[Daily Status Report]::: No errors  on:  %s " %(start_timestamp ) 
        content = ""  
        print "No Error found"
    
    return content,subject         

def send_report(valid_recipents_address, content, subject, filename):
    fromaddress = settings.SMTP_CONF["USERNAME"]
    mail.send_email(fromaddress, valid_recipents_address, content, filename, subject)
    