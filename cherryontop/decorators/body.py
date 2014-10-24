import functools

import cherrypy
import ujson

from cherryontop.errors import HTTPError, InvalidParameter, MissingParameter
from cherryontop.errors import PayloadError, RequestError, UnexpectedParameter


def validate_body(*a, **kw):
    allowed, required, validators = _get_checks(*a, **kw)

    def wrap(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            body = _deserialize_request_body()
            param_names = body.keys()

            # 1. all required parameters present?
            for param in required:
                if param not in param_names:
                    raise MissingParameter(param)

            # 2. all supplied parameters allowed?
            for param in param_names:
                if param not in allowed:
                    raise UnexpectedParameter(param)

            # 3. parameter values pass all tests?
            for param_name, test in validators:
                if param_name in param_names:
                    _validate_param(test, param_name, body[param_name])

            # if a body param and a query param match in name, only the body
            # param will be passed through
            kwargs.update(**body)

            return f(*args, **kwargs)
        return wrapped
    return wrap


def _get_checks(*args, **kwargs):
    required = kwargs.pop('require', [])
    required = set(required)

    allowed = kwargs.pop('allow', [])
    allowed = set(allowed)
    allowed |= required

    to_check = []

    for validator in args:
        param_name, tests = validator
        if isinstance(tests, (list, tuple,)):
            for test in tests:
                _check_validator(test)
                to_check.append((param_name, test,))
        else:
            _check_validator(tests)
            to_check.append(validator)

        allowed.add(param_name)

    return allowed, required, to_check


def _check_validator(test):
    if not (isinstance(test, type) or callable(test)):
        raise TypeError('validator must be callable')


def _deserialize_request_body():
    mimetype = cherrypy.request.headers.get('content-type')
    if mimetype != 'application/json':
        raise RequestError('Not JSON')

    body = cherrypy.request.body.read()
    if not body:
        return {}

    try:
        body = ujson.loads(body)
    except ValueError:
        raise PayloadError('Invalid JSON')

    return body


def _validate_param(test, param_name, value):
    if isinstance(test, type):
        if not isinstance(value, test):
            raise InvalidParameter(param_name)
    elif callable(test):
        if not test(value):
            raise InvalidParameter(param_name)
