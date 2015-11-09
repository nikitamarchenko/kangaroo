__author__ = 'nmarchenko'

import pika
import json
import sys
import libvirt
import os.path


from kangaroo.util import get_rabbit_connection_string

_MODULE = sys.modules[__name__]


def serve():
    connection = pika.BlockingConnection(pika.URLParameters(get_rabbit_connection_string()))
    channel = connection.channel()

    channel.queue_declare(queue='vm')

    print ' [*] Waiting for messages. To exit press CTRL+C'

    def callback(ch, method, properties, body):
        method, args, kwargs = json.loads(body)
        try:
            getattr(_MODULE, method)(*args, **kwargs)
        except libvirt.libvirtError as ex:
            print '[ERROR](libvirtError) {}'.format(ex)

    channel.basic_consume(callback, queue='vm', no_ack=True)

    channel.start_consuming()


def get_domain(name):
    conn = libvirt.open('qemu:///system')
    return conn.lookupByName(name)


def create(argv):
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(os.path.dirname(_MODULE.__file__)))
    template = env.get_template('template.xml')
    domain_xml = template.render(**argv)
    conn = libvirt.open('qemu:///system')
    conn.defineXML(domain_xml)


def delete(name):
    domain = get_domain(name)
    domain.undefine()


def on(name):
    domain = get_domain(name)
    domain.createWithFlags(0)


def off(name):
    domain = get_domain(name)
    domain.destroyFlags(0)


def reboot(name):
    domain = get_domain(name)
    domain.reboot()
