import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders 
import template
import settings
import tempfile

SMTP_CONF = {
             "MAIL_ENABLE": False,
             "MAIL_RECIPIENTS_OVERRIDE": False,
             "MOCK_MAIL_RECIPIENTS": [],
             "SERVER":"smtp.gmail.com",
             "PORT":587,
             "USERNAME":"logparserUtility@gmail.com",
             "PASSWORD":"log12345"
             }

def send_email(fromaddress, toaddresses, content, filename , subject = "", ):
    dir = settings.PROJECT_DIR          
    me = fromaddress
    you = toaddresses
    smtp_server = SMTP_CONF["SERVER"]
    smtp_username = SMTP_CONF["USERNAME"]
    smtp_password = SMTP_CONF["PASSWORD"]
    smtp_port = SMTP_CONF["PORT"] 
    msg = MIMEMultipart()
    msg['Subject'] ='["Daily Status Report]: %s'% ( subject)
    msg['From'] = me        
    msg['To'] =  you 
    html_content = MIMEText(content, 'html', _charset='utf-8') 
    msg.attach(html_content)
    part = MIMEBase('application', "octet-stream")
    f = filename
    part.set_payload( open(f,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part)                   
    reciepents = toaddresses.split(',') 
    server = smtplib.SMTP(smtp_server,smtp_port, local_hostname='logparserUtility@gmail.com') 
    server.starttls()
    server.login(smtp_username,smtp_password)
    server.sendmail(fromaddress,reciepents,msg.as_string())
    server.quit()
    os.remove(filename)      
    return True




