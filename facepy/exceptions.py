class FacepyError(Exception):
    """Base class for exceptions raised by Facepy."""

class FacebookError(FacepyError):
    """Class for errors returned by Facebook API."""
    def __init__(self, message, code):
        super(FacebookError, self).__init__(message)
        self.code = code

class HttpError(FacepyError):
    """Class for errors ocurred when there is problem with communication."""
