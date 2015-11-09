__author__ = 'nmarchenko'

from jsonschema import ValidationError
import pecan


def schema_validation_to_json(f):

    def wrapper(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except ValidationError as ex:
            pecan.response.status_int = 400
            return {'error': ex.message}

    return wrapper
