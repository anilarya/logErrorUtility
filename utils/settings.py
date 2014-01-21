import os
import ConfigParser

PROJECT_DIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read([os.path.abspath(PROJECT_DIR + '/utils/log_config.cfg')])
status = config.get("config_use", "status")
mode = config.get("mode", "m")
app_server = config.get("mode", "app")
recipient_email = config.get("local", "mailto")
path = config.get("local", "logpath")
apache_regex = config.get("app_web_server", "apache")
ngnix_regex = config.get("app_web_server", "ngnix")