class FacepyError(Exception):
    """Base class for exceptions raised by Facepy."""

    def __init__(self, message):
        self.message = message
