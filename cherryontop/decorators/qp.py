import functools
import inspect

import cherrypy
from cherrypy.lib.httputil import parse_query_string

from cherryontop.errors import InvalidParameter, UnexpectedParameter


def typecast_query_params(*a, **kw):
    allowed, cast_funcs = _get_checks(*a, **kw)

    def wrap(f):
        dynamic_url_args = _positional_arg_names(f)

        if set(allowed) & set(dynamic_url_args):  # disjoint?
            msg = 'query param and dynamic url component names cannot match'
            raise ValueError(msg)

        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            query_params = parse_query_string(cherrypy.request.query_string)

            # no param names conflict with dynamic url component names
            for param in query_params:
                if param in dynamic_url_args:
                    raise UnexpectedParameter(param)

            # all supplied parameters allowed?
            for param in query_params:
                if param not in allowed:
                    raise UnexpectedParameter(param)

            # typecast params
            for param, cast in cast_funcs:
                if param in query_params:
                    try:
                        query_params[param] = cast(query_params[param])
                    except ValueError:
                        raise InvalidParameter(param)

            kwargs.update(query_params)

            return f(*args, **kwargs)
        return wrapped
    return wrap


def _get_checks(*args, **kwargs):
    allowed = kwargs.pop('allow', [])
    allowed = set(allowed)

    to_cast = []

    for caster in args:
        param_name, func = caster
        if not callable(func):
            raise TypeError('cast func must be callable')

        allowed.add(param_name)
        to_cast.append(caster)

    return allowed, to_cast


def _positional_arg_names(f):
    spec = inspect.getargspec(f)
    args = spec.args
    num_positional = len(args) - len(spec.defaults)
    return args[:num_positional]
