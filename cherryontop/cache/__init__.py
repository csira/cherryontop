from cherryontop.cache.controller import icontrollers, register_controller
from cherryontop.cache.route import map_routes_for_controller, register_route


def map_all_routes(dispatcher):
    for cid, controller in icontrollers():
        map_routes_for_controller(cid, controller, dispatcher)


__all__ = ['map_all_routes', 'register_controller', 'register_route',]
