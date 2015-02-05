import functools
import uuid

import ujson

from cherryontop.cache import register_controller, register_route
from cherryontop.errors import error_response_handler


def _to_json(f):
    @functools.wraps(f)
    def wrap(*a, **kw):
        data = f(*a, **kw)
        return ujson.dumps(data)
    return wrap


def _setup_cp_config(cls):
    cp_config = getattr(cls, '_cp_config', {})
    if 'request.error_response' not in cp_config:
        cp_config['request.error_response'] = error_response_handler
        cls._cp_config = cp_config


class _Base(type):
    def __new__(cls, name, bases, dct):
        bases_of_this_type = [b for b in bases if isinstance(b, cls)]
        is_proper_subclass = len(bases_of_this_type) > 0

        if is_proper_subclass:  # skip for the base class
            cid = uuid.uuid4().hex

            for key, val in dct.items():
                if hasattr(val, '_cbs_routes'):  # handler?
                    for route, method in val._cbs_routes:
                        register_route(cid,
                                       route,
                                       val.__name__,
                                       conditions={'method': [method]})

                    dct[key] = _to_json(val)

        the_class = super(_Base, cls).__new__(cls, name, bases, dct)

        if is_proper_subclass:
            register_controller(cid, the_class)
            _setup_cp_config(the_class)

        return the_class


class Controller(object):

    __metaclass__ = _Base
