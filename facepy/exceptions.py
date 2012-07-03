class FacepyError(Exception):
    """Base class for exceptions raised by Facepy."""

    def __init__(self, message):
        self.message = message

class FacebookError(FacepyError):
    """Exception for Facebook errors."""

    def __init__(self, message=None, code=None):
        self.message = message
        self.code = code

class OAuthError(FacebookError):
    """Exception for Facebook errors specifically related to OAuth."""

class HTTPError(FacepyError):
    """Exception for transport errors."""

class SignedRequestError(FacepyError):
    """Exception for invalid signed requests."""
