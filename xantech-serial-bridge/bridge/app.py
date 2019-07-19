import os
import time

import json
import logging

from flask import Flask
from flask_restplus import Api, Resource

import models # bridge.models

log = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app=app, doc='/docs',
          title='Multi-Zone Audio Serial Bridge', version='0.1',
          description='REST interface for communicating with multi-zone audio controllers and amplifiers')

def run():
    import settings

    # FIXME: this should listen on 0.0.0.0 inside the Docker container
    app.config['SERVER_NAME'] = os.getenv('BRIDGE_SERVER_NAME', '127.0.0.1:5000')

    # FIXME: rework this...this should be YAML driven
    app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config['RESTPLUS_VALIDATE']        = settings.RESTPLUS_VALIDATE
    app.config['RESTPLUS_MASK_SWAGGER']    = settings.RESTPLUS_MASK_SWAGGER
    app.config['ERROR_404_HELP']           = settings.RESTPLUS_ERROR_404_HELP

    app.run(debug=settings.FLASK_DEBUG)

    # iterate over all configured interfaces and instatiate the endpoints
    for interface in configured_interfaces:
        endpoint = interface['endpoint']
        name = interface['name']

        # GET /<interface>
        # GET /<interface>/zones
        # FIXME: create object
        api.namespace(endpoint, description='Control interface for ' + name)
        app.register_blueprint(api, url_prefix='/' + endpoint)

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

if __name__ == '__main__':
    run()
