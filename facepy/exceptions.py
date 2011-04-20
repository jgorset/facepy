class FacepyError(Exception):
    """Base class for exceptions raised by Facepy."""
    pass
    
class APIUnavailableError(FacepyError): pass
class APIError(FacepyError): pass