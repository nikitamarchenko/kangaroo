__author__ = 'nmarchenko'

from pecan import expose
from pecan.rest import RestController
from utils import schema_validation_to_json
from jsonschema import validate
import kangaroo.vm.client as vm


_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "br": {
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
        "action": {
            "type": "string",
            "pattern": "^(on|off|reboot)$"
        },
    },
    "required": [
        "action",
    ],
    "additionalProperties": False
}


class Vms(RestController):

    @expose('json')
    @schema_validation_to_json
    def post(self, **data):
        validate(data, _POST_SCHEMA)
        vm.create(data)

    @expose('json')
    @schema_validation_to_json
    def put(self, name, **data):
        validate(data, _PUT_SCHEMA)
        getattr(vm, data['action'])(name)

    @expose('json')
    def delete(self, name):
        vm.delete(name)
