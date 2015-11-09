__author__ = 'nmarchenko'

import pika
import json
from kangaroo.util import get_rabbit_connection_string


def _send(data):
    connection = pika.BlockingConnection(pika.URLParameters(get_rabbit_connection_string()))
    channel = connection.channel()
    channel.queue_declare(queue='network')
    channel.basic_publish(exchange='', routing_key='network', body=json.dumps(data))
    connection.close()


def send(f):
    def wrapper(*args, **kwargs):
        _send((f.__name__, args, kwargs))
    return wrapper


@send
def create(name):
    pass


@send
def delete(name):
    pass


@send
def add_if(name, if_name):
    pass


@send
def delete_if(name, if_name):
    pass
