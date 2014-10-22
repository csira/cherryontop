import cherrypy
import ujson

from cherryontop.errors.base import CherryOnTopError, HTTPError
from cherryontop.errors.base import ProgrammingError
from cherryontop.errors.req import InvalidParameter, MissingParameter
from cherryontop.errors.req import PayloadError, RequestError
from cherryontop.errors.req import UnexpectedParameter


def _body(error, http_response_code):
    return ujson.dumps({
        'error': error.__class__.__name__,
        'http_response_code': http_response_code,
        'message': error.message,
    })


def _extra_headers(status):
    if status == 401:
        realm = 'Basic realm="auth required"'
        cherrypy.response.headers['www-authenticate'] = realm


def error_response_handler():
    _, e, _ = cherrypy._cperror._exc_info()
    status = e.http_response_code if isinstance(e, CherryOnTopError) else 500

    cherrypy.response.body = _body(e, status)
    cherrypy.response.headers['content-type'] = 'application/json'
    cherrypy.response.status = status
    _extra_headers(status)


__all__ = [
    'error_response_handler',
    'CherryOnTopError', 'HTTPError', 'InvalidParameter', 'MissingParameter',
    'PayloadError', 'ProgrammingError', 'RequestError', 'UnexpectedParameter',
]
