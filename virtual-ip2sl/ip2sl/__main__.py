import os
import yaml

import logging
import logging.config

import server

def setup_logging():
    """Setup logging configuration"""
    
    path = os.getenv('IP2SL_LOG_CONFIG', 'config/logging.yaml')
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        logging.debug(f"Read logging configuration from {path}")
    else:
        print(f"ERROR! Couldn't find logging configuration: {path}")
        logging.basicConfig(level=DEBUG)

setup_logging()
server.main()
