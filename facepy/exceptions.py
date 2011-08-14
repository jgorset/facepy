class FacepyError(Exception):
    """Base class for exceptions raised by Facepy."""
    pass

class SignedRequestError(FacepyError):
    """Exception raised for invalid signed_request processing."""
    pass

