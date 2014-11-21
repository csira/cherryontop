"""
1 - Hello World

This first sample app defines a single handler, opens a GET route
at '/', loads cherrypy config data from 'tutorial.conf', and starts
up a server with screen logging enabled.

$ python tutorial01.py
$ curl 0.0.0.0:8080 -v

* About to connect() to 0.0.0.0 port 8080 (#0)
*   Trying 0.0.0.0...
* Adding handle: conn: 0x7f97d0804000
* Adding handle: send: 0
* Adding handle: recv: 0
* Curl_addHandleToPipeline: length: 1
* - Conn 0 (0x7f97d0804000) send_pipe: 1, recv_pipe: 0
* Connected to 0.0.0.0 (0.0.0.0) port 8080 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.30.0
> Host: 0.0.0.0:8080
> Accept: */*
>
< HTTP/1.1 200 OK
< Date: Fri, 07 Nov 2014 23:56:33 GMT
< Content-Length: 26
< Content-Type: application/json
* Server CherryPy/3.6.0 is not blacklisted
< Server: CherryPy/3.6.0
<
* Connection #0 to host 0.0.0.0 left intact
{"message":"Hello world!"}

"""

import os

import cherryontop


class HelloWorld(cherryontop.Controller):

    @cherryontop.get('/')
    def hello_world(self):
        return {'message': 'Hello world!'}


if __name__ == '__main__':
    file_dir = os.path.dirname(os.path.realpath(__file__))
    conf = '%s/tutorial.conf' % file_dir

    cherryontop.start_server(conf, log_to_screen=True)
