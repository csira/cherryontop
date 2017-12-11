import cherrypy
import ujson

from cherryontop.errors import CherryOnTopError


def deserialize_request_body():
    try:
        body = cherrypy.request.body.read()
    except TypeError as e:
        # thrown if a) the request body has not yet been processed, or b) the
        # request method is not POST or PUT
        raise CherryOnTopError(e)

    if not body:
        return {}

    try:
        body = ujson.loads(body)
    except ValueError:
        raise CherryOnTopError("Invalid JSON")

    return body
