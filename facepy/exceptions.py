class FacepyError(Exception):
    """Base class for exceptions raised by Facepy."""

    def __init__(self, message):
        self.message = message

    def _get_message(self):
        return self._message

    def _set_message(self, message):
        self._message = message

    message = property(_get_message, _set_message)
