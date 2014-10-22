import functools

import cherrypy
import ujson

from cherryontop.errors import HTTPError, InvalidParameter, MissingParameter
from cherryontop.errors import PayloadError, ProgrammingError
from cherryontop.errors import RequestError, UnexpectedParameter


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


def _get_checks(*validators):
    allowed, required, to_check = set(), set(), []

    for validator in validators:
        if isinstance(validator, str):
            param_name = validator
        elif isinstance(validator, tuple):
            param_name, test = validator
            if test == 'required':
                required.add(param_name)
            elif isinstance(test, type) or callable(test):
                to_check.append(validator)
            else:
                raise ProgrammingError('cannot parse validator')
        else:
            raise ProgrammingError('cannot parse validator')

        allowed.add(param_name)

    return allowed, required, to_check


def _validate_param(test, param_name, value):
    if isinstance(test, type):
        if not isinstance(value, test):
            raise InvalidParameter(param_name)
    elif callable(test):
        if not test(value):
            raise InvalidParameter(param_name)


def validate_body(*validators):
    allowed, required, validators = _get_checks(*validators)

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
