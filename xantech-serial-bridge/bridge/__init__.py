import os
import logging.config

#logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
#logging.config.fileConfig(logging_conf_path)
logging.config.fileConfig("logging.conf")