__author__ = 'nmarchenko'

import pika
import json
from kangaroo.util import get_rabbit_connection_string
import sys
import subprocess


_MODULE = sys.modules[__name__]


def serve():
    connection = pika.BlockingConnection(pika.URLParameters(get_rabbit_connection_string()))
    channel = connection.channel()

    channel.queue_declare(queue='network')

    print ' [*] Waiting for messages. To exit press CTRL+C'

    def callback(ch, method, properties, body):
        method, args, kwargs = json.loads(body)
        getattr(_MODULE, method)(*args, **kwargs)

    channel.basic_consume(callback, queue='network', no_ack=True)

    channel.start_consuming()


def create(name):
    subprocess.call(['sudo', 'brctl', 'addbr', name])
    subprocess.call(['sudo', 'ip', 'link', 'set', 'up', 'dev', name])


def delete(name):
    subprocess.call(['sudo', 'ip', 'link', 'set', 'down', 'dev', name])
    subprocess.call(['sudo', 'brctl', 'addbr', name])


def add_if(name, if_name):
    subprocess.call(['sudo', 'brctl', 'addif', name, if_name])


def delete_if(name, if_name):
    subprocess.call(['sudo', 'brctl', 'delif', name, if_name])
