from flask_restplus import fields
from server.instance import server

zone = server.api.model('Zone', {
    'id': fields.Integer(description='Id'),
    'name': fields.String(required=True, min_length=1, max_length=100, description='Zone name')
})
