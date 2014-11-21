"""
2 - Additional routes

Any number of routes may be bound by defining additional handlers
wrapped with the `route`, `get`, `post`, `put`, or `delete`
decorators.

`route` is a special case only in that it provides support for
multiple methods.

It is worth mentioning here that it is completely safe to wrap the
same handler with multiple route decorators, e.g. `post_hello_world`
below.

Sample app 2 supports the following routes:
    GET     /
    POST    /
    POST    /other_post
    PUT     /
    DELETE  /
    GET     /other_get

"""

import os

import cherryontop
import cherrypy


class HelloWorld(cherryontop.Controller):

    @staticmethod
    def _render(handler_name):
        return {
            'message': 'Hello world!',
            'method': cherrypy.request.method,
            'handler': handler_name,
        }

    @cherryontop.get('/')
    def get_hello_world(self):
        return self._render('get_hello_world')

    @cherryontop.post('/')
    @cherryontop.post('/other_post')
    def post_hello_world(self):
        return self._render('post_hello_world')

    @cherryontop.route('/', methods=['PUT', 'DELETE'])
    @cherryontop.get('/other_get')
    def other_hello_world(self):
        return self._render('other_hello_world')


if __name__ == '__main__':
    file_dir = os.path.dirname(os.path.realpath(__file__))
    conf = '%s/tutorial.conf' % file_dir

    cherryontop.start_server(conf, log_to_screen=True)
