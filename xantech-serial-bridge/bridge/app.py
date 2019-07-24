import os
import time

import json
import yaml
import logging
import logging.config

import pprint
import hiyapyco # yaml

from flask import Flask
from flask_restplus import Api, Resource

import models # bridge.models

# FIXME: for dynamic import of modules
#   see  https://www.bnmetrics.com/blog/dynamic-import-in-python3
#from importlib import import_module

log = logging.getLogger(__name__)

VERSION = '0.1'

app = Flask(__name__)
api = Api(app=app, doc='/docs', title='Multi-Zone Audio Serial Bridge', version=VERSION,
          url="https://github.com/rsnodgrass/hassio-addons/tree/master/xantech-serial-bridge",
          description='REST interface for communicating with multi-zone audio controllers and amplifiers')

@api.route('/')
class BridgeInfo(Resource):
    def get(self):
        """
        Return details on all the multi-zone audio devices available
        """
        details = {
            "controllers": { "xantech8":   "Xantech 8-Zone Audio (Second Floor)",
                             "xantech8-2": "Xantech 8-Zone Audio (Basement)" }
        }
        return json.dumps(details)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

def setup_logging(
    default_path='logging.yaml',
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
        print("ERROR! Couldn't find logging configuration: " + path)
        logging.basicConfig(level=default_level)

setup_logging()

def load_config(config_file):
    with open(config_file, 'r') as stream:
        log.info("Loading configuration from %s", config_file)
        try:
            # FIXME: better loading configuration...
            config = hiyapyco.load('bridge/defaults.yaml',
                                   'bridge/interfaces/xantech8/config.yaml',
                                   'bridge/interfaces/monoprice6/config.yaml',
                                    config_file,
                                    method=hiyapyco.METHOD_MERGE,
                                    interpolate=True,
                                    failonmissingfiles=True)
            #config = yaml.safe_load(stream)
            log.debug("Loading configuration %s", config)
            return config
        except yaml.YAMLError as exc:
            print(exc)

def load_interface(name, config):
    # FIXME: load the code, then load the default configuration
    # see https://www.bnmetrics.com/blog/dynamic-import-in-python3
    log.error("Could not load interface %s", name)

# copy specified keys from YAML to the Flask app config
def yaml_to_flask_app_config(config, keys):
    for key in keys:
        app.config['key'] = config[key.lower()]

def run():
    config = load_config('bridge_config.yaml') # FIXME: allow env override?
    print(hiyapyco.dump(config))

    bridge_config = config['bridge'] 
    host = str(bridge_config['host']) # FIXME: allow env override?
    port = str(bridge_config['port']) # FIXME: allow env override?
    app.config['SERVER_NAME'] = host + '":' + port

    yaml_to_flask_app_config(config['restplus'], [ 'SWAGGER_UI_DOC_EXPANSION',
                                                   'RESTPLUS_VALIDATE',
                                                   'RESTPLUS_MASK_SWAGGER',
                                                   'ERROR_404_HELP' ])

    # iterate over all configured interfaces and instatiate the endpoints
    for interface in config['amplifiers']:
        log.info("Configuring equipment '%s'", interface)

        interface_type = 'xantech8'
        load_interface(interface_type)

        # FIXME: map the logical name to the interface type

        # merge in any default YAML configuration for each equipment

        #from .namespace1 import api as ns1

        # GET /<interface>
        # GET /<interface>/zones
        # FIXME: create object
       # ns = api.namespace(endpoint, description='Control interface for ' + name)
       # app.register_blueprint(ns, url_prefix='/' + endpoint)

    flask_debug = config['flask']['debug']
    app.run(debug=flask_debug)


if __name__ == '__main__':
    run()
