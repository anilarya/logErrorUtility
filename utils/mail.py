import smtplib 
from email.mime.text import MIMEText
import template
SMTP_CONF = {
             "MAIL_ENABLE": False,
             "MAIL_RECIPIENTS_OVERRIDE": False,
             "MOCK_MAIL_RECIPIENTS": [],
             "SERVER":"smtp.gmail.com",
             "PORT":587,
             "USERNAME":"logparserUtility@gmail.com",
             "PASSWORD":"log12345"
             }

def send_email(fromaddress,toaddresses,content,subject = "" ):
    me = fromaddress
    you = toaddresses
    smtp_server = SMTP_CONF["SERVER"]
    smtp_username = SMTP_CONF["USERNAME"]
    smtp_password = SMTP_CONF["PASSWORD"]
    smtp_port = SMTP_CONF["PORT"] 
    msg = MIMEText(content, 'html', _charset='utf-8')
    msg['Subject'] ='["Daily Status Report]: %s'% ( subject)
    msg['From'] = me        
    msg['To'] =  you     
    reciepents = toaddresses.split(',') 
    server = smtplib.SMTP(smtp_server,smtp_port, local_hostname='logparserUtility@gmail.com') 
    server.starttls()
    server.login(smtp_username,smtp_password) 
    server.sendmail(fromaddress,reciepents,msg.as_string())
    server.quit()
    return True


