__author__ = 'nmarchenko'


def create(session, argv):
    data = {'name': argv.name}

    if argv.br is not None:
        data['br'] = argv.br

    response = session.post('vms'.format(argv.name), data=data)
    response.raise_for_status()


def power_off(session, argv):
    response = session.put('vms/{}'.format(argv.name), data={'action': 'off'})
    response.raise_for_status()


def power_on(session, argv):
    response = session.put('vms/{}'.format(argv.name), data={'action': 'on'})
    response.raise_for_status()


def reboot(session, argv):
    response = session.put('vms/{}'.format(argv.name), data={'action': 'reboot'})
    response.raise_for_status()


def delete(session, argv):
    response = session.delete('vms/{}'.format(argv.name))
    response.raise_for_status()