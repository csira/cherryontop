import json

import cherrypy


class CherryOnTopError(Exception):

    status_code = 500


def error_response_handler():
    _, e, _ = cherrypy._cperror._exc_info()

    if isinstance(e, CherryOnTopError):
        status = e.status_code
        message = e.message
    else:
        status = 500
        message = ""

    cherrypy.response.headers["content-type"] = "application/json"
    cherrypy.response.status = status
    cherrypy.response.body = json.dumps({
        "error": e.__class__.__name__,
        "status_code": status,
        "message": message})

    if status == 401:
        realm = 'xBasic realm="auth required"'
        cherrypy.response.headers["www-authenticate"] = realm
