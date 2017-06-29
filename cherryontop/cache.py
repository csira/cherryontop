import uuid

from cherryontop.errors import CherryOnTopError

_routes = []


def register_route(method, pattern, f):
    route = {
        "route": pattern,
        "action": f.__name__,
        "conditions": {"method": [method]},
        "name": uuid.uuid4().hex}

    _test_for_duplicate_func_name(f)
    _test_for_duplicate_pattern(pattern)
    _routes.append((f, route,))


def _test_for_duplicate_func_name(func):
    if func.__name__ in [f.__name__ for f in handlers()]:
        raise CherryOnTopError("duplicate handler function name found: {}".format(func.__name__))


def _test_for_duplicate_pattern(pattern):
    if pattern in [args["route"] for args in routes()]:
        raise CherryOnTopError("duplicate pattern: {}".format(pattern))


def handlers():
    return [i[0] for i in _routes]


def routes():
    return [i[1] for i in _routes]
