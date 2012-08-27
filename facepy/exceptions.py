class FacepyError(Exception):
    """Base class for exceptions raised by Facepy."""


class FacebookError(FacepyError):
    """Exception for Facebook errors."""
    def __init__(self, message=None, code=None):
        self.message = message
        self.code = code

        if self.code:
            message = '[%s] %s' % (self.code, self.message)

        super(FacebookError, self).__init__(message)


class OAuthError(FacebookError):
    """Exception for Facebook errors specifically related to OAuth."""


class HTTPError(FacepyError):
    """Exception for transport errors."""


class SignedRequestError(FacepyError):
    """Exception for invalid signed requests."""
