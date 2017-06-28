import functools
import json

import cherrypy

from cherryontop.cache import handlers, routes
from cherryontop.errors import error_response_handler


def dispatcher_factory():
    controller = _controller_factory()
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    for route in routes():
        print route
        print
        dispatcher.connect(controller=controller, **route)

    return dispatcher


def _controller_factory():

    class Base(type):
        def __new__(cls, name, bases, dct):
            for f in handlers():
                dct[f.__name__] = _jsonify( _remove_cls_arg(f) )
            return super(Base, cls).__new__(cls, name, bases, dct)

    class Controller(object):
        __metaclass__ = Base
        _cp_config = {"request.error_response": error_response_handler}

    return Controller


def _remove_cls_arg(f):
    @functools.wraps(f)
    def wrapper(cls, *a, **kw):
        return f(*a, **kw)
    return wrapper


def _jsonify(f):
    @functools.wraps(f)
    def wrapper(*a, **kw):
        data = f(*a, **kw)
        return json.dumps(data)
    return wrapper
