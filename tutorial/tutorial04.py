"""
4 - Query parameters

While standard cherrypy handling for query parameters is still
intact, you may define a signature and cast them to appropriate
types with the `typecast_query_params` decorator. It takes any
number of (param, func) tuples, where `param` is the name of
the query parameter and `func` is a callable that casts the
given value to the desired type.

The `UnexpectedParameter` error is raised when any unspecified
parameter is provided. To bypass this behavior for a paremeter
that needs no typecasting, specify a list of allowed parameters
with the `allow` keyword argument. When `UnexpectedParameter`
is raised, the name of the offending parameter is returned in
the response payload's 'message' key.

$ curl '0.0.0.0:8080'
{"message":"Hello you!"}

$ curl '0.0.0.0:8080?name=chris'
{"message":"Hello chris!"}

$ curl '0.0.0.0:8080?name=chris&a=1&b=2'
{"a":1,"message":"Hello chris!","b":2.0}

$ curl '0.0.0.0:8080?name=chris&a=1&b=2&c=3'
{"message":"c","http_response_code":400,"error":"UnexpectedParameter"}

"""

import os

import cherryontop


class HelloWorldController(cherryontop.Controller):

    @cherryontop.get('/')
    @cherryontop.typecast_query_params(('a', int,),
                                       ('b', float,),
                                       allow=['name'])
    def hello_world(self, name=None, **kw):
        kw['message'] = 'Hello %s!' % (name or 'you')
        return kw


if __name__ == '__main__':
    file_dir = os.path.dirname(os.path.realpath(__file__))
    conf = '%s/tutorial.conf' % file_dir

    cherryontop.start_server(conf, log_to_screen=True)
