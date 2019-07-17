import logging

from flask_restplus import Api

log = logging.getLogger(__name__)

# FIXME: inject name and version from elsewhere!
api = Api(title='Serial Smart Bridge',
          version='0.0.1',
          description='RESTful APIs for controlling hardware devices connected via serial connections')