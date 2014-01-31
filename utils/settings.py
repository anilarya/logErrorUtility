import os 

PROJECT_DIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

#===================================================user-Info================================================================
#name of your project
project = 'PROJECT -NAME'

#s3 environment _id 
env_id = 'Environment-Id'

#path where log is available for parsing, having extention: ".log"
logpath = '/var/log/ngnix'

#For example  :  apche, ngnix etc
app_web_server = 'apache' 

#mailing lists
recipient_email =  'anil.kumar@gmail.com,naga@hashedin.com'

#yours SMTP configurations
SMTP_CONF = {
             "MAIL_ENABLE": False,
             "MAIL_RECIPIENTS_OVERRIDE": False,
             "MOCK_MAIL_RECIPIENTS": [],
             "SERVER":"smtp.gmail.com",
             "PORT":587,
             "USERNAME":"username",  # for expample@gmail.com
             "PASSWORD":"password",   #1213
             }

#===================================================END user-Info============================================================== 


#=========================================log regular-expressions for application web server ==================================
ngnix_regex = '^(?P<hostname>[\w.]*) (?P<clientip>[\d.]+) (?P<user>[\w-]+) (?P<application>[\w-]+) '+\
                        '(?P<request>\[\d+/\w+/\d+\:\d+\:\d+\:\d+[ \t]\-\d+\]) "(?P<method>GET|POST|PUT|DELETE|HEAD|TRACE|OPTIONS) (?P<url>.*?)'+\
                        ' (?P<protocol>HTTP/1.[01])" (?P<status>\d+) (?P<bytes_sent>\d+) (?P<request_time>[\d.-]+) (?P<upstream_response_time>[\d.-]+)'+\
                        ' (?P<hma_exec_time>[\d.-]+) (?P<mongo_exec_time>[\d.-]+) (?P<audit_response_time>[\d.-]+) (?P<queries_count>[\d.-]+) "(?P<user_agent>.*?)"$'

apache_regex ='^(?P<clientip>[\d.]+) (?P<user>[\w-]+) (?P<application>[\w-]+) (?P<request>.+) "(?P<method>GET|POST|PUT|DELETE|HEAD|TRACE|OPTIONS) (?P<url>.*?) (?P<protocol>HTTP/1.[01])" (?P<status>\d+) (?P<bytes_sent>\d+) "(?P<referer>.*)" "(?P<user_agent>.*?)"$'
