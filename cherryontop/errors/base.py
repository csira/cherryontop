class CherryOnTopError(Exception):

    http_response_code = 500


class HTTPError(CherryOnTopError):
    pass
