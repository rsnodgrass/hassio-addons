import os
import time

import yaml
import json
import logging.config

from bridge import settings

from flask import Flask, Blueprint
from flask_restplus import Api

Version = "0.0.1"

app = Flask(__name__)
api = Api(title='Serial Smart Bridge',
          version=Version,
          description='RESTful APIs for controlling hardware devices connected via serial connections')

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

# read from bridge-config.yaml
Modules = { 'xantech':         'xantech-mrc88',
            'radiora':         'radiora-classic',
            'intermatic-pool': 'intermatic-pe653' }

def configure_app(flask_app):
    # FIXME: rework this...to allow ENV override
    flask_app.config['SERVER_NAME']              = '127.0.0.1:5000'
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE']        = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER']    = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP']           = settings.RESTPLUS_ERROR_404_HELP

def add_module_apis(flask_app, modules):
    for api_name, module_name in modules:
        # FIXME: should support multiple modules (by name, defaulted to module name)
        blueprint = Blueprint(api_name, __name__, url_prefix='/api/' + api_name)
        api.init_app(blueprint)

        # dynamically load module
        package_name = "package." + module_name
        # mod = __import__(package_name, fromlist=[''])
        # mod.doSomething()

        # FIXME: now dynamically add all the mapped values
        #  api.add_namespace(manager_zones_namespace)
        flask_app.register_blueprint(blueprint)

def initialize_app(flask_app):
     configure_app(flask_app)
     add_module_apis(flask_app, Modules)

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


def main():
    initialize_app(app)

    log.info('>>>>> Starting Serial Smart Bridge v' + Version + ' at http://{}/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()
