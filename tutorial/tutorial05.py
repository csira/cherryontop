"""
5 - Request bodies

While POST & PUT bodies are generally accessed via
`cherrypy.request.body`, CherryOnTop provides the
`validate_body` decorator to extract body parameters,
validate them, and stuff them into the method as keyword
arguments.

`validate_body` takes any number of (param_name, validator)
tuples, where `param` is the JSON key and `validator` may
be a callable or a type. Callables must take the JSON value
as an input and return a bool, where any False immediately
triggers an `InvalidParameter` error. If a type is specified
instead and the given value is not an instance of the
declared type, `InvalidParameter` is thrown as well.

Like `typecast_query_params`, all expected parameters must
be declared, else `UnexpectedParameter` will be thrown. The
`allow` keyword argument is still available to bypass this.

Any parameter listed in the `require` argument array will
be subjected to one additional validation step: every
request MUST specify this parameter, else `MissingParameter`
is raised.

NB: A side effect of injecting both body parameters and
query parameters as keyword arguments is the possibility
for same-named parameters to overwrite one another. For
this reason, it is recommended you avoid such naming
conflicts within a single handler.

Caveat: since CherryPy passes query parameters as keyword arguments
by default, `typecast_query_params` must be listed above `validate_body`
in cases where you must use them both. E.g.

$ curl 0.0.0.0:8080 -H 'content-type:application/json' -d '{"name":"chris"}'
{"message":"Hello chris!"}

$ curl 0.0.0.0:8080 -H 'content-type:application/json' -H "content-length:0" -X POST
{"message":"name","http_response_code":400,"error":"MissingParameter"}

$ curl 0.0.0.0:8080 -H 'content-type:application/json' -d '{"name":"chris","underwear_size":"m","foo":"bar"}'
{"message":"Hello chris!","foo":"bar","underwear_size":"m"}

$ curl 0.0.0.0:8080 -H 'content-type:application/json' -d '{"name":"chris","underwear_size":"M"}'
{"message":"underwear_size","http_response_code":400,"error":"InvalidParameter"}

"""

import os

import cherryontop


UNDERWEAR_SIZES = ['s', 'm', 'l']


class HelloWorldController(cherryontop.Controller):

    @cherryontop.post('/')
    @cherryontop.validate_body(('name', unicode,),
                               ('underwear_size', lambda i: i in UNDERWEAR_SIZES,),
                               allow=('foo',),
                               require=('name',))
    def hello_world(self, name=None, **kw):
        kw['message'] = 'Hello %s!' % (name or 'you')
        return kw


if __name__ == '__main__':
    file_dir = os.path.dirname(os.path.realpath(__file__))
    conf = '%s/tutorial.conf' % file_dir

    cherryontop.start_server(conf, log_to_screen=True)
