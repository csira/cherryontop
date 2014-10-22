def route(uri_pattern, method='GET', methods=None):
    methods = methods or [method]
    new_routes = [(uri_pattern, method.upper(),) for method in methods]

    def wrap(f):
        routes = getattr(f, '_cbs_routes', [])
        routes += new_routes
        f._cbs_routes = routes
        return f

    return wrap


def delete(uri_pattern):
    return route(uri_pattern, method='DELETE')


def get(uri_pattern):
    return route(uri_pattern, method='GET')


def post(uri_pattern):
    return route(uri_pattern, method='POST')


def put(uri_pattern):
    return route(uri_pattern, method='PUT')
