import json

import cherrypy


class CherryOnTopError(Exception):

    status_code = 500

    def __init__(self, *a, **kw):
        Exception.__init__(self, *a)
        self.meta = kw.pop("meta", None)
        self.kwargs = kw


def error_response_handler():
    _, e, _ = cherrypy._cperror._exc_info()

    if isinstance(e, CherryOnTopError):
        status = e.status_code
        message = e.message
        meta = e.meta
    else:
        status = 500
        message = ""
        meta = None

    cherrypy.response.headers["content-type"] = "application/json"
    cherrypy.response.status = status
    cherrypy.response.body = json.dumps({
        "error": e.__class__.__name__,
        "status_code": status,
        "message": message,
        "meta": meta})

    if status == 401:
        realm = 'xBasic realm="auth required"'
        cherrypy.response.headers["www-authenticate"] = realm
