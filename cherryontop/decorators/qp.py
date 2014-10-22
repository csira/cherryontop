import functools

from cherryontop.errors import InvalidParameter, ProgrammingError
from cherryontop.errors import UnexpectedParameter


def _get_checks(*params_or_funcs):
    allowed, to_cast = set(), []

    for param_or_func in params_or_funcs:
        if isinstance(param_or_func, str):
            param_name = param_or_func
        elif isinstance(param_or_func, tuple):
            param_name, func = param_or_func
            if not callable(func):
                raise ProgrammingError('cannot parse cast function')
            to_cast.append(param_or_func)
        else:
            raise ProgrammingError('cannot parse cast function')

        allowed.add(param_name)

    return allowed, to_cast


def typecast_query_params(*params_or_funcs):
    allowed, cast_funcs = _get_checks(*params_or_funcs)

    def wrap(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            # all supplied parameters allowed?
            for param in kwargs:
                if param not in allowed:
                    raise UnexpectedParameter(param)

            # typecast params
            for param_name, cast in cast_funcs:
                if param_name in kwargs:
                    try:
                        kwargs[param_name] = cast(kwargs[param_name])
                    except ValueError:
                        raise InvalidParameter(param_name)

            return f(*args, **kwargs)
        return wrapped
    return wrap
