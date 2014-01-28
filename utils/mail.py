import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders 
import template
import settings
import tempfile


def send_email(fromaddress, toaddresses, content="", filenames=None , subject = ""):   
    '''
    Utility to send mail to given recipients address having attached files and error pi-charts
    '''      
    me = fromaddress
    you = toaddresses
    smtp_server = settings.SMTP_CONF["SERVER"]
    smtp_username = settings.SMTP_CONF["USERNAME"]
    smtp_password = settings.SMTP_CONF["PASSWORD"]
    smtp_port = settings.SMTP_CONF["PORT"] 
    msg = MIMEMultipart()
    msg['Subject'] ='[ %s ] %s'% (settings.project, subject)
    msg['From'] = me        
    msg['To'] =  you 
    html_content = MIMEText(content, 'html', _charset='utf-8') 
    msg.attach(html_content)
    part = MIMEBase('application', "octet-stream")
    part2 = MIMEBase('application', "octet-stream")
    f1 = filenames[0]
    f2 = filenames[1] 
    if os.path.getsize(f1) !=0 : 
        part.set_payload( open(f1,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="slow_urls.txt"')
        msg.attach(part)
    if os.path.getsize(f2) !=0 :
        part2.set_payload( open(f2,"rb").read() )
        Encoders.encode_base64(part2)
        part2.add_header('Content-Disposition', 'attachment; filename="5xx_errors.txt"')
        msg.attach(part2)             
    reciepents = toaddresses.split(',') 
    server = smtplib.SMTP(smtp_server,smtp_port, local_hostname='logparserUtility@gmail.com') 
    server.starttls()
    server.login(smtp_username,smtp_password)
    server.sendmail(fromaddress,reciepents,msg.as_string())
    server.quit()
    os.remove(filenames[0]) 
    os.remove(filenames[1])     
    return True