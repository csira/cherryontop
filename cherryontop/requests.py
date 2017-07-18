import json

import cherrypy

from cherryontop.errors import CherryOnTopError


def deserialize_request_body():
    body = cherrypy.request.body.read()
    if not body:
        return {}

    try:
        body = json.loads(body)
    except ValueError:
        raise CherryOnTopError("Invalid JSON")

    return body
