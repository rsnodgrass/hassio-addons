from flask_restplus import fields
from bridge.api.restplus import api

# zone = api.model('Zone details', {
#    'id': fields.Integer(readOnly=True, description='The unique identifier of a zone'),
#    'name': fields.String(required=True, description='Zone Name'),
#     'zone': fields.Integer(required=True, description='Zone Number'),
#     'system': fields.Integer(required=True, description='System Number'),
#     'state': fields.String(required=True, description='Zone State'),
#     'zonetypeid': fields.Integer(attribute='zonetype.id'),
#     'zonetype': fields.String(attribute='zonetype.name'),
# })

# zones = api.inherit('Zones', zone, {
#     'zones': fields.List(fields.Nested(zone))
# })

# zonetype = api.model('Zone type', {
#     'id': fields.Integer(readOnly=True, description='The unique identifier of a zone type'),
#     'name': fields.String(required=True, description='Zone type name'),
# })

# zonetype_with_zones = api.inherit('Zone Type with zones', zonetype, {
#     'zones': fields.List(fields.Nested(zone))
# })
