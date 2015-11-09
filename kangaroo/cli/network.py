__author__ = 'nmarchenko'


def create(session, argv):
    response = session.post('networks', data={'name': argv.name})
    response.raise_for_status()


def remove(session, argv):
    response = session.delete('networks/{}'.format(argv.name))
    response.raise_for_status()


def addif(session, argv):
    response = session.put('networks/{}'.format(argv.name), data={'if': argv.interface, 'action': 'add'})
    response.raise_for_status()


def delif(session, argv):
    response = session.put('networks/{}'.format(argv.name), data={'if': argv.interface, 'action': 'delete'})
    response.raise_for_status()
