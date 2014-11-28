"""
3 - Dynamic routes

Dynamic routes in CherryOnTop may be specified by placing a colon
prior to each dynamic component, then passing those elements into
the method as positional or keyword arguments.

"""

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
    cherryontop.start_server(log_to_screen=True)
