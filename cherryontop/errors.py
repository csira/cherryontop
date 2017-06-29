import json

import cherrypy


class CherryOnTopError(Exception):

    status_code = 500


def error_response_handler():
    _, e, _ = cherrypy._cperror._exc_info()
    status = e.status_code if isinstance(e, CherryOnTopError) else 500

    cherrypy.response.headers["content-type"] = "application/json"
    cherrypy.response.status = status
    cherrypy.response.body = json.dumps({
        "error": e.__class__.__name__,
        "status_code": status,
        "message": e.message})

    if status == 401:
        realm = 'xBasic realm="auth required"'
        cherrypy.response.headers["www-authenticate"] = realm
