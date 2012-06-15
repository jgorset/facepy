class FacepyError(Exception):
    """Base class for exceptions raised by Facepy."""

    def _get_message(self):
        return self._message

    def _set_message(self, message):
        self._message = message

    message = property(_get_message, _set_message)
