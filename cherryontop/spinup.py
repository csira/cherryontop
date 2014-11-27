import cherrypy

from cherryontop.cache import map_all_routes


def _create_dispatcher():
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    map_all_routes(dispatcher)
    return dispatcher


def _daemonize():
    daemonizer = cherrypy.process.plugins.Daemonizer(cherrypy.engine)
    daemonizer.subscribe()
    sig_handler = cherrypy.process.plugins.SignalHandler(cherrypy.engine)
    sig_handler.subscribe()


def _set_default_headers():
    headers = cherrypy.config.get('tools.response_headers.headers', [])
    headers.append(('Content-Type', 'application/json'))

    cherrypy.config.update({
        'tools.response_headers.headers': headers,
        'tools.response_headers.on': True,
    })


def _setup_global_config(config=None):
    if config:  # dictionary or path to config file
        cherrypy.config.update(config)
    _set_default_headers()


def start_server(host='0.0.0.0',
                 port=8080,
                 threads=20,
                 autoreload=False,
                 log_to_screen=False,
                 path_to_access_log=None,
                 path_to_error_log=None,
                 **kwargs):
    conf = {
        'engine.autoreload_on': autoreload,
        'log.screen': log_to_screen,
        'server.socket_host': host,
        'server.socket_port': port,
        'server.thread_pool': threads,
    }

    if path_to_access_log:
        conf['log.access_file'] = path_to_access_log
    if path_to_error_log:
        conf['log.error_file'] = path_to_error_log

    strict_start_server(config=conf, **kwargs)


def strict_start_server(config=None, root='/', daemonize=False):
    _setup_global_config(config)

    if daemonize:
        _daemonize()

    app_config = {
        root: {'request.dispatch': _create_dispatcher()},
    }

    cherrypy.quickstart(None, root, config=app_config)
