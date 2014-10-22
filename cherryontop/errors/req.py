from cherryontop.errors.base import HTTPError


class RequestError(HTTPError):

    http_response_code = 400


class PayloadError(RequestError):
    pass


class InvalidParameter(PayloadError):
    pass


class MissingParameter(PayloadError):
    pass


class UnexpectedParameter(PayloadError):
    pass
