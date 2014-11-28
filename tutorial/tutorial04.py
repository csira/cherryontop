"""
4 - Exceptions

CherryOnTop exception classes plug into the cherrypy engine to
return JSON error descriptions to the client. That is, when a
subclass of `CherryOnTopError` is raised e.g.

    raise cherryontop.errors.HTTPError('something bad happened')

and not explicitly caught, the following cascade kicks in:

  - the HTTP response code is set to <exception>.http_response_code
  - the HTTP response type is set to 'application/json'
  - a JSON payload is rendered and returned, e.g.

    {
        'error': 'HTTPError',
        'http_response_code': 500,
        'message': 'something bad happened',
    }

$ curl "0.0.0.0:8080/broken" -v

* About to connect() to 0.0.0.0 port 8080 (#0)
*   Trying 0.0.0.0...
* Adding handle: conn: 0x7fc573804000
* Adding handle: send: 0
* Adding handle: recv: 0
* Curl_addHandleToPipeline: length: 1
* - Conn 0 (0x7fc573804000) send_pipe: 1, recv_pipe: 0
* Connected to 0.0.0.0 (0.0.0.0) port 8080 (#0)
> GET /broken HTTP/1.1
> User-Agent: curl/7.30.0
> Host: 0.0.0.0:8080
> Accept: */*
>
< HTTP/1.1 500 Internal Server Error
< Date: Sun, 09 Nov 2014 14:48:27 GMT
< Content-Length: 81
< Content-Type: application/json
* Server CherryPy/3.6.0 is not blacklisted
< Server: CherryPy/3.6.0
<
* Connection #0 to host 0.0.0.0 left intact
{"message":"this handler is broken","http_response_code":500,"error":"HTTPError"}

"""

import cherryontop


class HelloWorld(cherryontop.Controller):

    @cherryontop.get('/broken')
    def im_broken(self):
        raise cherryontop.errors.HTTPError('this handler is broken')


if __name__ == '__main__':
    cherryontop.start_server(log_to_screen=True)
