"""
3 - Dynamic routes

Dynamic routes in CherryOnTop may be specified by placing a colon
prior to each dynamic component, then passing those elements into
the method as positional or keyword arguments.

For consistency, only optional parameters should be passed as
keyword arguments. Required parameters should appear positionally
and in the same order they appear in the URL.

"""

import os

import cherryontop


class HelloWorld(cherryontop.Controller):

    @cherryontop.get('/hello')
    @cherryontop.get('/hello/:name')
    def hello_world(self, name='world'):
        return {'message': 'Hello %s!' % name}

    @cherryontop.get('/goodbye/:name')
    def goodbye(self, name):
        return {'message': 'So long %s!' % name}


if __name__ == '__main__':
    file_dir = os.path.dirname(os.path.realpath(__file__))
    conf = '%s/tutorial.conf' % file_dir

    cherryontop.start_server(conf, log_to_screen=True)
