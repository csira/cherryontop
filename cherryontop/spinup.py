import cherrypy

from cherryontop.dispatcher import dispatcher_factory
from cherryontop.discover import scan


def start_server(host="0.0.0.0", port=8080, threads=20, autoreload=False,
        log_to_screen=False, path_to_access_log=None, path_to_error_log=None,
        daemonize=False, autoscan=True, scan_root="."):

    if autoscan:
        scan(scan_root)

    config = {
        "engine.autoreload.on": autoreload,
        "log.screen": log_to_screen,
        "requests.show_tracebacks": False,
        "server.socket_host": host,
        "server.socket_port": port,
        "server.thread_pool": threads,
    }

    if path_to_access_log:
        config["log.access_file"] = path_to_access_log
    if path_to_error_log:
        config["log.error_file"] = path_to_error_log

    cherrypy.config.update(config)
    _set_default_headers()

    if daemonize:
        _daemonize()

    app_config = {"/": {"request.dispatch": dispatcher_factory()}}
    cherrypy.quickstart(None, "/", config=app_config)


def _daemonize():
    daemonizer = cherrypy.process.plugins.Daemonizer(cherrypy.engine)
    daemonizer.subscribe()
    sig_handler = cherrypy.process.plugins.SignalHandler(cherrypy.engine)
    sig_handler.subscribe()


def _set_default_headers():
    headers = cherrypy.config.get("tools.response_headers.headers", [])
    headers.append(("Content-Type", "application/json"))

    cherrypy.config.update({
        "tools.response_headers.headers": headers,
        "tools.response_headers.on": True,
    })
