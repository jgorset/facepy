import facepy


class FacebookTestUser(object):
    def __init__(self, **kwargs):
        fields = ('id', 'access_token', 'login_url', 'email', 'password')
        for field in fields:
            setattr(self, field, kwargs[field])
        self.graph = facepy.GraphAPI(self.access_token)


class TestUserManager(object):
    def __init__(self, app_id, app_secret):
        access_token = facepy.get_application_access_token(app_id, app_secret)
        self.graph = facepy.GraphAPI(access_token)
        self.app_id = app_id

    def create_user(self, **parameters):
        """ creates facebook test user

            Valid parameters (with default values):
              installed = true
              name = FULL_NAME
              locale = en_US
              permissions = read_stream

        """

        url =  "%s/accounts/test-users" % self.app_id
        return FacebookTestUser(**self.graph.post(url, **parameters))

    def delete_user(self, user):
        self.graph.delete(str(user.id))


class TestUser(object):
    def __init__(self, manager, **user_params):
        self.manager = manager
        self.user_params = user_params

    def __enter__(self):
        self._user = self.manager.create_user(**self.user_params)
        return self._user

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        self.manager.delete_user(self._user)
