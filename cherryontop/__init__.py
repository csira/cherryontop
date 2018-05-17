import functools
import importlib
import os
import uuid

import cherrypy
import ujson


__all__ = [
    "get", "post", "put", "delete", "route", "start_server", "CherryOnTopError",
    "deserialize_request_body", "get_header", "set_header", "get_cookie", "set_cookie"]


def start_server(
        host="0.0.0.0", port=8080, threads=20, daemonize=False, autoreload=False,
        log_to_screen=False, path_to_access_log=None, path_to_error_log=None,
        autoscan=True, scan_root="."):

    if autoscan:
        _scan(scan_root)

    headers = cherrypy.config.get("tools.response_headers.headers", [])
    headers.append(("Content-Type", "application/json"))

    config = {
        "engine.autoreload.on": autoreload,
        "log.screen": log_to_screen,
        "request.show_tracebacks": False,
        "server.socket_host": host,
        "server.socket_port": port,
        "server.thread_pool": threads,
        "tools.response_headers.headers": headers,
        "tools.response_headers.on": True}

    if path_to_access_log:
        config["log.access_file"] = path_to_access_log
    if path_to_error_log:
        config["log.error_file"] = path_to_error_log

    cherrypy.config.update(config)

    if daemonize:
        cherrypy.process.plugins.Daemonizer(cherrypy.engine).subscribe()
        cherrypy.process.plugins.SignalHandler(cherrypy.engine).subscribe()

    app_config = {"/": {"request.dispatch": _dispatcher_factory()}}
    cherrypy.quickstart(None, "/", config=app_config)


def _scan(path):
    for dir_name, subdir_list, file_list in os.walk(path):
        if "__pycache__" in dir_name:
            continue
        if "__init__.py" not in file_list:
            continue
        if dir_name.startswith("./env") or dir_name.startswith("./.git"):
            continue

        for file_name in file_list:
            if not file_name.endswith(".py"):
                continue

            path = "/".join([dir_name, file_name])
            path = path[2:-3]  # trim ./ off front and .py off end
            path = path.replace("/", ".")
            importlib.import_module(path)




def route(method, pattern):
    def wrap(f):
        _register_route(method.upper(), pattern, f)
        return f
    return wrap


get = functools.partial(route, "get")
post = functools.partial(route, "post")
put = functools.partial(route, "put")
delete = functools.partial(route, "delete")


_handlers = []
_routes = []


def _register_route(method, pattern, f):
    if f.__name__ in (h.__name__ for h in _handlers):
        raise ValueError("duplicate handler function name: {}".format(f.__name__))

    for route in _routes:
        if method == route["conditions"]["method"][0] and pattern == route["route"]:
            raise ValueError("duplicate pattern: {} {}".format(method, pattern))

    _handlers.append(f)
    _routes.append({
        "route": pattern,
        "action": f.__name__,
        "conditions": {"method": [method]},
        "name": uuid.uuid4().hex})


def _dispatcher_factory():
    controller = _controller_factory()
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    for route in _routes:
        dispatcher.connect(controller=controller, **route)
    return dispatcher


def _controller_factory():

    class Base(type):
        def __new__(cls, name, bases, dct):
            for f in _handlers:
                dct[f.__name__] = staticmethod(_jsonify(f))
            return super(Base, cls).__new__(cls, name, bases, dct)

    class Controller(object):
        __metaclass__ = Base
        _cp_config = {"request.error_response": _unhandled_error_trap}

    return Controller


def _jsonify(f):
    @functools.wraps(f)
    def wrapper(*a, **kw):
        data = f(*a, **kw)
        return ujson.dumps(data)
    return wrapper




class CherryOnTopError(cherrypy.HTTPError):

    status_code = 500

    def __init__(self, message="", meta=None):
        super(CherryOnTopError, self).__init__(self.status_code)
        self.message = message
        self.meta = meta

    def set_response(self):
        """Formats responses for handled exceptions. Tracebacks are suppressed from the error log."""
        super(CherryOnTopError, self).set_response()
        _throw(self)


def _unhandled_error_trap():
    """Captures and formats responses for unhandled (i.e. non-HTTPError) exceptions.

    Though trapped, tracebacks for these exceptions will be logged to the
    error_file (if configured).

    This is NOT reached when a cherrypy.HTTPError is raised.

    """
    _, e, _ = cherrypy._cperror._exc_info()
    _throw(e)


def _throw(e):
    status_code = getattr(e, "status_code", 500)
    cherrypy.response.status = status_code

    body = ujson.dumps({
        "error": e.__class__.__name__,
        "status_code": status_code,
        "message": getattr(e, "message", ""),
        "meta": getattr(e, "meta", None)})
    cherrypy.response.body = body
    cherrypy.response.headers["content-length"] = len(body)
    cherrypy.response.headers["content-type"] = "application/json"

    if status_code == 401:
        cherrypy.response.headers["www-authenticate"] = 'xBasic realm="auth required"'




def deserialize_request_body():
    try:
        body = cherrypy.request.body.read()
    except TypeError as e:
        # thrown if a) the request body has not yet been processed, or b) the
        # request method is not POST or PUT
        raise CherryOnTopError(e)

    if not body:
        return {}

    try:
        body = ujson.loads(body)
    except ValueError:
        raise CherryOnTopError("Invalid JSON")

    return body


def get_header(name):
    return cherrypy.request.headers.get(name)


def set_header(name, value):
    cherrypy.response.headers[name] = value


def get_cookie(name):
    cookie = cherrypy.request.cookie.get(name)
    return cookie.value if cookie else None


def set_cookie(name, val, **morsels):
    cherrypy.response.cookie[name] = val
    for k, v in morsels.iteritems():
        cherrypy.response.cookie[name][k] = v
