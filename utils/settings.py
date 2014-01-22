import os 


PROJECT_DIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

#path where log is available for parsing
logpath = '/var/log/ngnix'

#mailing lists
recipient_email =  'anil.kumar@hashedin.com'

#settings for remote  
pemfile = '~/.ssh/Platform_Dev.pem'
gateway = 'ec2-user@gateway.hmadev.com' 

#apche, ngnix etc
app_web_server = 'apache'   

#log regular expressions for application web server 
ngnix_regex = '^(?P<hostname>[\w.]*) (?P<clientip>[\d.]+) (?P<user>[\w-]+) (?P<application>[\w-]+) '+\
                        '(?P<request>\[\d+/\w+/\d+\:\d+\:\d+\:\d+[ \t]\-\d+\]) "(?P<method>GET|POST|PUT|DELETE|HEAD|TRACE|OPTIONS) (?P<url>.*?)'+\
                        ' (?P<protocol>HTTP/1.[01])" (?P<status>\d+) (?P<bytes_sent>\d+) (?P<request_time>[\d.-]+) (?P<upstream_response_time>[\d.-]+)'+\
                        ' (?P<hma_exec_time>[\d.-]+) (?P<mongo_exec_time>[\d.-]+) (?P<audit_response_time>[\d.-]+) (?P<queries_count>[\d.-]+) "(?P<user_agent>.*?)"$'

apache_regex ='^(?P<clientip>[\d.]+) (?P<user>[\w-]+) (?P<application>[\w-]+) (?P<request>.+) "(?P<method>GET|POST|PUT|DELETE|HEAD|TRACE|OPTIONS) (?P<url>.*?) (?P<protocol>HTTP/1.[01])" (?P<status>\d+) (?P<bytes_sent>\d+) "(?P<referer>.*)" "(?P<user_agent>.*?)" (?P<response_time>[\d.-]+)$'
