import cherrypy

from cherryontop import Controller, get, post, route
from cherryontop import typecast_query_params, validate_body
from cherryontop.errors import HTTPError


class MyController(Controller):

    # _cp_config = {'x': 7}

    @get('/test')
    def test(self):
        return {'data': 'hello'}

    @post('/testpost')
    @validate_body(('a', float,), require=['b'])
    def test_post(self, **kwargs):
        return kwargs

    @get('/break')
    def busted(self):
        raise HTTPError('woo')

    @route('/multi', methods=['get', 'POST'])
    def multi(self):
        return {'method': cherrypy.request.method}

    @route('/qp')
    @typecast_query_params(('a', float),
                           ('b', float),
                           ('c', int),
                           ('c', bool))
    def qp_test(self, **kwargs):
        return kwargs
