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
    _test_for_duplicate_pattern(method, pattern)
    _routes.append((f, route,))


def _test_for_duplicate_func_name(func):
    if func.__name__ in (f.__name__ for f in handlers()):
        raise ValueError("duplicate handler function name found: {}".format(func.__name__))


def _test_for_duplicate_pattern(method, pattern):
    if any((method, pattern) == val for val in _pattern_iter()):
        raise ValueError("duplicate pattern: {}".format(pattern))


def _pattern_iter():
    for _, route in _routes:
        yield route["conditions"]["method"][0], route["route"]


def handlers():
    return (i[0] for i in _routes)


def routes():
    return (i[1] for i in _routes)
