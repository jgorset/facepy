from facepy import GraphAPI

class User(object):
    def __init__(self, id, access_token, login_url, email, password):
        self.id = id
        self.access_token = access_token
        self.login_url = login_url
        self.email = email
        self.password = password

        self.graph = GraphAPI(access_token)

    @classmethod
    def create(self, application_id, access_token, **parameters):
        """
        Create a new Facebook test user.

        :param application_id: A string describing the Facebook application ID.
        :param access_token: A string describing the application's access token.
        :param name: An optional string describing the user's name (defaults to a generated name).
        :param permissions: An optional list describing permissions.
        :param locale: An optional string describing the user's locale (defaults to ``en_US``).
        :param installed: A boolean describing whether the user has installed your application (defaults to ``True``).
        """
        return User(**GraphAPI(access_token).post('%s/accounts/test-users' % application_id, **parameters))

    def delete(self):
        """
        Delete the test user.
        """
        self.graph.delete(self.id)

class TestUser(object):
    def __init__(self, manager, **user_params):
        self.manager = manager
        self.user_params = user_params

    def __enter__(self):
        self._user = self.manager.create_user(**self.user_params)
        return self._user

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        self.manager.delete_user(self._user)
