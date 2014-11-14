import os

import cherrypy

from cherryontop import map_all_routes
from cherryontop import start_server

import miniapp.controllers


if __name__ == '__main__':
    file_dir = os.path.dirname(os.path.realpath(__file__))
    conf = '%s/cp.conf' % file_dir

    start_server(conf, log_to_screen=True)
