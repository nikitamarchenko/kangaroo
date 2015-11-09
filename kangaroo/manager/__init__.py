__author__ = 'nmarchenko'


import sys
from gunicorn.app.wsgiapp import WSGIApplication


def main():
    sys.argv += ['kangaroo.manager.api:application', '-c', '/etc/kangaroo/kangaroo-api-gunicorn.py']
    WSGIApplication("%(prog)s [OPTIONS]").run()
