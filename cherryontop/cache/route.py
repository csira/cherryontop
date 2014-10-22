from collections import defaultdict
import uuid


_registry = defaultdict(list)


def register_route(cid, route, handler_name, conditions=None):
    _registry[cid].append(dict(
        route=route,
        action=handler_name,
        conditions=conditions,
        name=uuid.uuid4().hex,
    ))


def map_routes_for_controller(cid, controller, dispatcher):
    for kwargs in _registry[cid]:
        dispatcher.connect(controller=controller, **kwargs)
