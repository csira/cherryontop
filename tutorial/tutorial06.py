"""
6 - Request bodies

For handlers expecting JSON dictionary payloads, CherryOnTop
provides the `validate_body` decorator to extract parameters,
validate them, and stuff them into the method as keyword arguments.

It takes any number of (param_name, validator) tuples, where
`param_name` is the key and `validator` may be a callable or
type. Callables must take the parameter value as an input and
return a bool (a False immediately triggers an `InvalidParameter`
error), and types indicate we should test the given value is
an instance of the specified type (`InvalidParameter` also thrown
if not).

Like `typecast_query_params` all expected parameters must be
declared, else `UnexpectedParameter` is thrown. Use the `allow`
keyword argument to bypass this.

The new keyword argument `require` is available here too. Any
parameter listed in the array but not provided in the request
body will trigger a `MissingParameter` error.

NB: Injecting both body parameters and query parameters as
keyword arguments leads to the possibility for same-named
parameters to overwrite one another. Hence, it is recommended
you avoid naming conflicts across body and query parameters
within a single handler.

Caveat: since cherrypy passes query parameters as keyword
arguments by default, `typecast_query_params` must be listed
above `validate_body` any time they are used together.

$ curl 0.0.0.0:8080 -H 'content-type:application/json' -d '{"name":"chris"}'
{"message":"Hello chris!"}

$ curl 0.0.0.0:8080 -H 'content-type:application/json' -H "content-length:0" -X POST
{"message":"name","http_response_code":400,"error":"MissingParameter"}

$ curl 0.0.0.0:8080 -H 'content-type:application/json' -d '{"name":"chris","underwear_size":"m","foo":"bar"}'
{"message":"Hello chris!","foo":"bar","underwear_size":"m"}

$ curl 0.0.0.0:8080 -H 'content-type:application/json' -d '{"name":"chris","underwear_size":"M"}'
{"message":"underwear_size","http_response_code":400,"error":"InvalidParameter"}

"""

import cherryontop


UNDERWEAR_SIZES = ['s', 'm', 'l']


class HelloWorld(cherryontop.Controller):

    @cherryontop.post('/')
    @cherryontop.validate_body(('name', unicode,),
                               ('underwear_size', lambda i: i in UNDERWEAR_SIZES,),
                               allow=('foo',),
                               require=('name',))
    def hello_world(self, name=None, **kw):
        kw['message'] = 'Hello %s!' % (name or 'you')
        return kw


if __name__ == '__main__':
    cherryontop.start_server(log_to_screen=True)
