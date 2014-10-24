import functools

from cherryontop.errors import InvalidParameter, UnexpectedParameter


def typecast_query_params(*a, **kw):
    allowed, cast_funcs = _get_checks(*a, **kw)

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
