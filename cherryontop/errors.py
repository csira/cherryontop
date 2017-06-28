import json

import cherrypy


class CherryOnTopError(Exception):

    http_response_code = 500


def error_response_handler():
    _, e, _ = cherrypy._cperror._exc_info()
    status = e.http_response_code if isinstance(e, CherryOnTopError) else 500

    cherrypy.response.headers["content-type"] = "application/json"
    cherrypy.response.status = status
    cherrypy.response.body = json.dumps({
        "error": e.__class__.__name__,
        "http_response_code": status,
        "message": e.message})

    if status == 401:
        realm = 'xBasic realm="auth required"'
        cherrypy.response.headers["www-authenticate"] = realm
