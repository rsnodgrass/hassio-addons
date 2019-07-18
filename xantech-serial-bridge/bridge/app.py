import os
import time

import yaml
import json
import logging

from flask import Flask
from flask_restplus import Api

log = logging.getLogger(__name__)

Version = '0.0.1'

app = Flask(__name__)
api = Api(app)

def run():
    _initialize_app(app)

    log.info('>>>>> Starting Serial Smart Bridge v' + Version + ' at http://{}/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

    def _configure_app(flask_app):
        # FIXME: rework this...to allow ENV override
        flask_app.config['SERVER_NAME']              = '127.0.0.1:5000'
        flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
        flask_app.config['RESTPLUS_VALIDATE']        = settings.RESTPLUS_VALIDATE
        flask_app.config['RESTPLUS_MASK_SWAGGER']    = settings.RESTPLUS_MASK_SWAGGER
        flask_app.config['ERROR_404_HELP']           = settings.RESTPLUS_ERROR_404_HELP


    def _initialize_app(flask_app):
        configure_app(flask_app)

    # importlib.import_module(name, package=None)

    @app.route('/')
    def index():
        # FIXME: should modules actually just be REST endpoints /xantech, etc
        details = {
            'version': Version,
            'modules': Modules
        }
        return json.dumps(details)

    # Expose dynamic binding API (if available)
    @app.route('/module/api/hass')
    def api():
        return "Return HASS API yaml configuration!"

# ... then dynamically sensors/lights/switches/etc get configured!
# ... only implement specific to HA, let someone else do SmartThings!
#  ...  perhaps have GET /xantech/api/<style>    GET /xantech/api/hass

# GET /
#   returns all exposed modules (auto-discover)

# GET /<module>
#   returns APIs

if __name__ == '__main__':
    log.info('>>>>> Starting Serial Smart Bridge v' + Version + ' at http://{}/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)