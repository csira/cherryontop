"""
3 - Dynamic routes

CherryOnTop supports dynamic routes in a common fashion: dynamic
URL components should be specified with a preceding colon, then
passed into the method as positional or keyword arguments.

For consistency's sake, it is recommended only optional parameters
be specified as keyword arguments. Required route parameters should
appear positionally and in the same order they appear in the URL.
(Suggestions only, neither strictly enforced.)

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
