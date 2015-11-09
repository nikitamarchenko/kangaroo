__author__ = 'nmarchenko'


import argparse
import os
import requests
import json

import vm
import network


def wrap(f):
    def wrapper(*args, **kwargs):
        self, endpoint = args[0], args[1]
        # if 'data' in kwargs:
        #     kwargs['data'] = json.dumps(kwargs['data'])
        #
        kwargs['data'] = json.dumps(kwargs.get('data'))
        return getattr(super(Session, self), f.__name__)(self._url(endpoint), **kwargs)
    return wrapper


class Session(requests.Session):

    def __init__(self, host, port):
        super(Session, self).__init__()
        self.headers = {"content-type": "application/json"}
        self.host = host
        self.port = port

    def _url(self, endpoint):
        return 'http://{}:{}/{}'.format(self.host, self.port, endpoint)

    @wrap
    def post(self, endpoint, **kwargs):
        pass

    @wrap
    def delete(self, endpoint, **kwargs):
        pass

    @wrap
    def put(self, endpoint, **kwargs):
        pass


def entry_point():
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', required=False, help='HOST', default=os.environ.get('KANGAROO_API_HOST', '127.0.0.1'))
    parser.add_argument('--port', required=False, help='PORT', default=os.environ.get('KANGAROO_API_PORT', '8080'))

    subparsers = parser.add_subparsers(help='sub-command help')

    parser_vm = subparsers.add_parser('vm', help='vm help')
    subparsers_vm = parser_vm.add_subparsers(help='sub-command help')

    vm_create = subparsers_vm.add_parser('create', help='create help')
    vm_create.add_argument('name', help='vm name')
    vm_create.add_argument('--br', help='bridge name')
    vm_create.set_defaults(func=vm.create)

    for command in ['delete', 'power-on', 'power-off', 'reboot']:
        vm_command = subparsers_vm.add_parser(command, help='{} help'.format(command))
        vm_command.add_argument('name', help='vm name')
        vm_command.set_defaults(func=getattr(vm, command.replace('-', '_')))

    parser_net = subparsers.add_parser('net', help='net help')
    subparsers_net = parser_net.add_subparsers(help='sub-command help')

    for command in ['create', 'remove']:
        net_command = subparsers_net.add_parser(command, help='{} help'.format(command))
        net_command.add_argument('name', help='bridge name')
        net_command.set_defaults(func=getattr(network, command))

    for command in ['addif', 'delif']:
        net_command = subparsers_net.add_parser(command, help='{} help'.format(command))
        net_command.add_argument('name', help='bridge name')
        net_command.add_argument('interface', help='interface name')
        net_command.set_defaults(func=getattr(network, command))

    args = parser.parse_args()

    args.func(Session(args.host, args.port), args)
