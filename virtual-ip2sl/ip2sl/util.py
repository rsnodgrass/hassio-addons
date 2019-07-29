import logging
import logging.config

import os
import sys
import yaml

log = logging.getLogger(__name__)

def get_host(config):
    # must be externally accessible and routable IP (not 0.0.0.0 or localhost)
    host = '127.0.0.1' # invalid default except for testing

    if ('ip2sl' in config and 'ip' in config['ip2sl']):
        host = config['ip2sl']['ip']

    # allow overridding discovered/configured IP address with ENV variable
    host = os.getenv('IP2SL_SERVER_HOST', host) 
    return host

def setup_logging(
    default_path='config/logging.yaml',
    default_level=logging.INFO
):
    """Setup logging configuration"""
    path = os.getenv('IP2SL_LOG_CONFIG', default_path)
    
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

        log = logging.getLogger(__name__)
        log.debug(f"Read logging configuration from {path}: {config}")
    else:
        print(f"ERROR! Couldn't find logging configuration: {path}")
        logging.basicConfig(level=default_level)

def read_config(config_file='config/default.yaml'):
    config_file = os.getenv('IP2SL_CONFIG', config_file) # ENV variable overrides all

    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            sys.stderr.write(f"FATAL! {exc}")
            sys.exit(1)

def get_with_default(config, key):
    if key not in config:
        config[key] = DEFAULT_CONFIG[key] # update the config with default if missing
    return config[key]