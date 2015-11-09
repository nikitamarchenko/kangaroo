__author__ = 'nmarchenko'

from pecan import expose

from networks import Networks
from vms import Vms


class RootController(object):
    def __init__(self):
        self.networks = Networks()
        self.vms = Vms()

    @expose('json')
    def notfound(self):
        return {'error': 'not found'}