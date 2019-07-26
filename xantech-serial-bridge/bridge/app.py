import os
import time

import re
import json
import yaml
import logging
import logging.config
from pathlib import Path

import hiyapyco # yaml

from flask import Flask
from flask_restplus import Api, Resource

import models # bridge.models

# FIXME: for dynamic import of modules
#   see  https://www.bnmetrics.com/blog/dynamic-import-in-python3
#from importlib import import_module

VERSION = '0.1'

app = Flask(__name__)
api = Api(app=app, doc='/docs', title='Multi-Zone Audio Serial Bridge', version=VERSION,
          url="https://github.com/rsnodgrass/hassio-addons/tree/master/xantech-serial-bridge",
          description='API to multi-zone audio controllers and amplifiers')

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

# discover what hardware interfaces are available
def discover_interfaces():
    interfaces = []
    for filename in Path('bridge/interfaces/').glob('**/config.yaml'):
        m = re.search("bridge/interfaces/(?P<interface>.+)/config.yaml", str(filename))
        if m:
            interface = m.group('interface')
            log.debug("Discovered interface '%s'", interface)
            interfaces.append(interface)
    return interfaces
INTERFACES = discover_interfaces()

def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            config_files = ['config/default.yaml']
            for interface in INTERFACES:
                config_files.append(f"bridge/interfaces/{interface}/config.yaml")
            config_files.append(config_file)

            log.debug("Loading configuration from: %s", config_files)
            config = hiyapyco.load(config_files,
                                   method=hiyapyco.METHOD_MERGE,
                                   interpolate=True,
                                   failonmissingfiles=True)

            #config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            sys.stderr.write(f"FATAL! {exc}")
            sys.exit(1)

def load_interface(config):
    # FIXME: load the code, then load the default configuration
    # see https://www.bnmetrics.com/blog/dynamic-import-in-python3
    print(config)
    log.error("Could not load interface %s", config['name'])


        # FIXME: map the logical name to the interface type

        # merge in any default YAML configuration for each equipment

        #from .namespace1 import api as ns1




# copy specified keys from YAML to the Flask app config
def yaml_to_flask_app_config(config, keys):
    for key in keys:
        app.config['key'] = config[key.lower()]

def main():
    config = load_config('bridge_config.yaml') # FIXME: allow env override?
    #print(hiyapyco.dump(config))

    bridge_config = config['bridge'] 
    host = os.getenv('BRIDGE_HOST', bridge_config['host'])
    port = int(os.getenv('BRIDGE_PORT', bridge_config['port']))
    
    yaml_to_flask_app_config(config['restplus'], [ 'SWAGGER_UI_DOC_EXPANSION',
                                                   'VALIDATE',
                                                   'MASK_SWAGGER',
                                                   'ERROR_404_HELP' ])



    # iterate over all configured interfaces and instatiate the endpoints
    for interface in config['amplifiers']:
        log.info("Configuring equipment '%s'", interface)
        conf = config['amplifiers'][interface]
        conf['id'] = interface # inject the interface name as the id

        load_interface(conf)

        # GET /<interface>
        # GET /<interface>/zones
        # FIXME: create object
       # ns = api.namespace(endpoint, description='Control interface for ' + name)
       # app.register_blueprint(ns, url_prefix='/' + endpoint)

    flask_debug = config['flask']['debug']
    app.run(debug=flask_debug, host=host, port=port)

@api.route('/f')
class BridgeInfo(Resource):
    def get(self):
        """
        Return details on all the control interfaces available
        """
        details = {
            "controllers": {
                "xantech8": { 
                    "name": "Xantech 8-Zone Audio (Second Floor)",
                    "url": "/xantech8/<slug>" },
                "xantech8-2": {
                    "name": "Xantech 8-Zone Audio (Basement)",
                    "url": "/xantech8/<slug2>"
                }
            }
        }
        return json.dumps(details)


if __name__ == '__main__':
    main()
