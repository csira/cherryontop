from functools import partial

from cherryontop.cache import register_route


def route(method, pattern):
    def wrap(f):
        register_route(method.upper(), pattern, f)
        return f
    return wrap


get = partial(route, "get")
post = partial(route, "post")
put = partial(route, "put")
delete = partial(route, "delete")
