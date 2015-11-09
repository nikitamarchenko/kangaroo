__author__ = 'nmarchenko'

import pecan
from pecan import expose
from pecan.rest import RestController
from jsonschema import validate
from utils import schema_validation_to_json

from kangaroo.network import client as network

_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
    },
    "required": [
        "name",
    ],
    "additionalProperties": False
}

_PUT_SCHEMA = {
    "type": "object",
    "properties": {
        "if": {
            "type": "string",
        },
        "action": {
            "type": "string",
            "pattern": "^(add|delete)$"
        },
    },
    "required": [
        "if",
        "action",
    ],
    "additionalProperties": False
}


class Networks(RestController):

    @expose('json')
    @schema_validation_to_json
    def post(self, **data):
        validate(data, _POST_SCHEMA)
        network.create(data['name'])

    @expose('json')
    @schema_validation_to_json
    def put(self, name, **data):
        validate(data, _PUT_SCHEMA)
        getattr(network, '{}_if'.format(data['action']))(name, data['if'])

    @expose('json')
    def delete(self, name):
        network.delete(name)

