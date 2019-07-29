import os
import logging

log = logging.getLogger(__name__)

def get_host(config):
    # must be externally accessible and routable IP (not 0.0.0.0 or localhost)
    host = '127.0.0.1' # invalid default except for testing

    if ('ip2sl' in config and 'ip' in config['ip2sl']):
        host = config['ip2sl']['ip']

    # allow overridding discovered/configured IP address with ENV variable
    host = os.getenv('IP2SL_SERVER_HOST', host) 
    return host