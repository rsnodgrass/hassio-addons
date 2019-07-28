#!/usr/local/bin/python3

import os
import yaml

import logging
import logging.config

import server

def setup_logging(
    default_path='config/logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CONFIG'
):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        print(f"ERROR! Couldn't find logging configuration: {path}")
        logging.basicConfig(level=default_level)

setup_logging()
log = logging.getLogger(__name__)

if __name__ == '__main__':
  server.main()

