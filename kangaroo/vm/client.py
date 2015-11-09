__author__ = 'nmarchenko'

import pika
import json
from kangaroo.util import get_rabbit_connection_string


def _send(data):
    connection = pika.BlockingConnection(pika.URLParameters(get_rabbit_connection_string()))
    channel = connection.channel()
    channel.queue_declare(queue='vm')
    channel.basic_publish(exchange='', routing_key='vm', body=json.dumps(data))
    connection.close()


def send(f):
    def wrapper(*args, **kwargs):
        _send((f.__name__, args, kwargs))
    return wrapper


@send
def create(argv):
    pass


@send
def delete(name):
    pass


@send
def on(name):
    pass


@send
def off(name):
    pass


@send
def reboot(name):
    pass
