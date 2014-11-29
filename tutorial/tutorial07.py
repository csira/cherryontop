"""
7 - Starting the server

As you've seen in the tutorials so far, it's trivial to spin
up CherryOnTop apps by calling `start_server`. This tutorial
illustrates additional options you may pass to `start_server`,
as well as the preferred way to pass cherrypy-style configs.

"""

import os

import cherryontop


class HelloWorld(cherryontop.Controller):

    @cherryontop.get('/')
    def hello_world(self):
        return {'message': 'Hello world!'}


if __name__ == '__main__':
    file_dir = os.path.dirname(os.path.realpath(__file__))
    access_log = '%s/access.log' % file_dir
    error_log = '%s/error.log' % file_dir


    # quick and easy - no config file but options for
    # common parameters

    cherryontop.start_server(host='127.0.0.1',    # default: 0.0.0.0
                             port=8123,           # default: 8080
                             threads=10,          # default: 20
                             autoreload=True,     # default: False
                             log_to_screen=True,  # default: False
                             path_to_access_log=access_log,
                             path_to_error_log=error_log)


    # an equivalent example - how to drive servers using
    # cherrypy config files

    config_file = '%s/tutorial.conf' % file_dir
    cherryontop.strict_start_server(config_file)


    # equivalently, a cherrypy config dict

    config_data = {
        'engine.autoreload_on': True,
        'log.access_file': access_log,
        'log.error_file': error_log,
        'log.screen': True,
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8123,
        'server.thread_pool': 10,
    }
    cherryontop.strict_start_server(config_data)
