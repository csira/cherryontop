_registry = {}


def register_controller(cid, controller):
    _registry[cid] = controller


def icontrollers():
    return _registry.iteritems()
