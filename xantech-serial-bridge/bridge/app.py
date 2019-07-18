import os
import time

import json
import logging

from flask import Flask
from flask_restplus import Api

log = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

def run():
    import bridge.settings as settings

    # FIXME: this should listen on 0.0.0.0 inside the Docker container
    app.config['SERVER_NAME'] = os.getenv('BRIDGE_SERVER_NAME', '127.0.0.1:5000')

    # FIXME: rework this...to allow ENV override
    app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config['RESTPLUS_VALIDATE']        = settings.RESTPLUS_VALIDATE
    app.config['RESTPLUS_MASK_SWAGGER']    = settings.RESTPLUS_MASK_SWAGGER
    app.config['ERROR_404_HELP']           = settings.RESTPLUS_ERROR_404_HELP

    app.run(debug=settings.FLASK_DEBUG)

@app.route('/')
class BridgeInfo(Resource):
    def get(self):
        details = {}
        return json.dumps(details)

if __name__ == '__main__':
    run()
