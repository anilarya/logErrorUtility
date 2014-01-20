import render
import mail

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

def get_count_information(count, request):
    if  request['status'] >='500' and request['status'] < '600':
        count["5xx"]['5xx_Counts'] += 1 
    elif  request['status'] >='400'and request['status'] < '500':
        count["4xx"]['4xx_Counts'] += 1  
    elif  request['status'] >='200' and request['status'] < '300' :
        count["2xx"]['2xx_Counts'] += 1
        
    count['total']['total_Count'] += 1
    return count


def report_generate(count_dict, start_timestamp):
    if count_dict['4xx']["4xx_Counts"] != 0 or count_dict['5xx']["5xx_Counts"] != 0:
        subject = " ::  %d Messages Failed" %(count_dict['5xx']["5xx_Counts"] +  count_dict['4xx']["4xx_Counts"])
        content = render.get_email_html_body(start_timestamp, count_dict)
    elif count_dict['4xx']["4xx_Counts"] == 0 and count_dict['5xx']["5xx_Counts"] == 0 :
        subject = ":: No errors  on:  %s " %(start_timestamp ) 
        content = ""  
        print "No Error found"
    
    return content,subject         

def send_report(valid_recipents_address,content,subject):
    fromaddress = mail.SMTP_CONF["USERNAME"]
    mail.send_email(fromaddress,valid_recipents_address, content,subject)
    