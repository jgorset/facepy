class FacepyError(Exception):
    """Base class for exceptions raised by Facepy."""


class FacebookError(FacepyError):
    """Exception for Facebook errors."""
    def __init__(self, message=None, code=None, error_data=None, error_subcode=None,
                 is_transient=None, error_user_title=None, error_user_msg=None,
                 fbtrace_id=None):
        self.message = message
        self.code = code
        self.error_data = error_data
        self.error_subcode = error_subcode
        self.is_transient = is_transient
        self.error_user_title = error_user_title
        self.error_user_msg = error_user_msg
        self.fbtrace_id = fbtrace_id

        if self.code:
            message = '[%s] %s' % (self.code, self.message)

        super(FacebookError, self).__init__(message)


class OAuthError(FacebookError):
    """Exception for Facebook errors specifically related to OAuth."""


class HTTPError(FacepyError):
    """Exception for transport errors."""


class SignedRequestError(FacepyError):
    """Exception for invalid signed requests."""


class InternalFacebookError(FacebookError):
    """Exception for Facebook internal server error."""
