class Error(Exception):
    pass


class Unavailable(Error):
    pass


class APIError(Error):
    pass


class ValidationError(Error):
    pass
