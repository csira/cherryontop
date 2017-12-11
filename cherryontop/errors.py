import cherrypy
import ujson


class CherryOnTopError(cherrypy.HTTPError):

    status_code = 500

    def __init__(self, message="", meta=None):
        super(CherryOnTopError, self).__init__(self.status_code)
        self.message = message
        self.meta = meta

    def set_response(self):
        """Formats responses for handled exceptions. Tracebacks are suppressed from the error log."""
        super(CherryOnTopError, self).set_response()
        _throw(self)


def unhandled_error_trap():
    """Captures and formats responses for unhandled (i.e. non-HTTPError) exceptions.

    Though trapped, tracebacks for these exceptions will be logged to the
    error_file (if configured).

    This is NOT reached when a cherrypy.HTTPError is raised.

    """
    _, e, _ = cherrypy._cperror._exc_info()
    _throw(e)


def _throw(e):
    status_code = getattr(e, "status_code", 500)
    cherrypy.response.status = status_code

    body = ujson.dumps({
        "error": e.__class__.__name__,
        "status_code": status_code,
        "message": getattr(e, "message", ""),
        "meta": getattr(e, "meta", None)})
    cherrypy.response.body = body
    cherrypy.response.headers["content-length"] = len(body)
    cherrypy.response.headers["content-type"] = "application/json"

    if status_code == 401:
        cherrypy.response.headers["www-authenticate"] = 'xBasic realm="auth required"'
