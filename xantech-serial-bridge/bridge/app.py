import os
import time

import json
import yaml
import hiyapyco # yaml
import logging
import logging.config

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

def load_config(config_file='bridge_config.yaml'):

    with open(config_file, 'r') as stream:
        log.info("Loading configuration from %s", config_file)
        try:
            config = hiyapyco.load('bridge/defaults.yaml', config_file)

            #config = yaml.safe_load(stream)
            print config
            log.debug("Loading configuration %s", config)
        except yaml.YAMLError as exc:
            print(exc)

def load_modules(name, config):
    # FIXME: load the code, then load the default configuration
    # see https://www.bnmetrics.com/blog/dynamic-import-in-python3

def run():
    import settings

    # Default to listen on all interefaces. Note this may be insecure if run outside the
    # context of a Docker container since this is accessible on all network interfaces.
    app.config['SERVER_NAME'] = os.getenv('BRIDGE_SERVER_NAME', '0.0.0.0:5000')

    # FIXME: rework this...this should be YAML driven for consistency
    app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config['RESTPLUS_VALIDATE']        = settings.RESTPLUS_VALIDATE
    app.config['RESTPLUS_MASK_SWAGGER']    = settings.RESTPLUS_MASK_SWAGGER
    app.config['ERROR_404_HELP']           = settings.RESTPLUS_ERROR_404_HELP

    # FIXME: dynamicalyl load based on configuration
    config = load_config()
#    if config['bridge']['port']:
#        port = config['bridge']['port']

    port = config['port']
    host = config['host']

    # iterate over all configured interfaces and instatiate the endpoints
    for interface in config['amplifiers']:
        log.info("Configuring equipment '%s'", interface)

        # merge in any default YAML configuration for each equipment

        module = import_module('.' )


        #endpoint = interface['endpoint']
       # name = interface['name']

        #from .namespace1 import api as ns1

        # GET /<interface>
        # GET /<interface>/zones
        # FIXME: create object
       # ns = api.namespace(endpoint, description='Control interface for ' + name)
       # app.register_blueprint(ns, url_prefix='/' + endpoint)

    app.run(debug=settings.FLASK_DEBUG)


if __name__ == '__main__':
    run()
