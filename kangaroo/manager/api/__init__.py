__author__ = 'nmarchenko'


from pecan.deploy import deploy


application = deploy('/etc/kangaroo/kangaroo-api-pecan.py')
