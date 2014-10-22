import cherrypy

from cherryontop.cache import map_all_routes


def _create_dispatcher():
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    map_all_routes(dispatcher)
    return dispatcher


def _setup_cp_config(path_to_cherrypy_config,
                     path_to_access_log=None,
                     path_to_error_log=None,
                     log_to_screen=False):
    if path_to_access_log:
        cherrypy.config.update({'log.access_file': path_to_access_log})
    if path_to_error_log:
        cherrypy.config.update({'log.error_file': path_to_error_log})
    cherrypy.config.update({'log.screen': log_to_screen})
    cherrypy.config.update(path_to_cherrypy_config)


def _daemonize():
    daemonizer = cherrypy.process.plugins.Daemonizer(cherrypy.engine)
    daemonizer.subscribe()
    sig_handler = cherrypy.process.plugins.SignalHandler(cherrypy.engine)
    sig_handler.subscribe()


def start_server(path_to_conf, root='/', daemonize=False, **kwargs):
    _setup_cp_config(path_to_conf, **kwargs)
    if daemonize:
        _daemonize()

    conf = {root: {'request.dispatch': _create_dispatcher()}}
    cherrypy.quickstart(None, root, config=conf)
