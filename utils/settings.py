import os
import ConfigParser

PROJECT_DIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read([os.path.abspath(PROJECT_DIR + '/utils/log_config.cfg')])