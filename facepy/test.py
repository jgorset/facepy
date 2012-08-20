from facepy import GraphAPI

class User(object):
    def __init__(self, id, access_token, login_url, email, password):
        self.id = id
        self.access_token = access_token
        self.login_url = login_url
        self.email = email
        self.password = password

        self.graph = GraphAPI(access_token)

class TestUserManager(object):
    def __init__(self, application_id, access_token):
        self.application_id = application_id
        self.access_token = access_token
        self.graph = GraphAPI(access_token)

    def create_user(self, **parameters):
        """ creates facebook test user

            Valid parameters (with default values):
              installed = true
              name = FULL_NAME
              locale = en_US
              permissions = read_stream

        """

        url =  "%s/accounts/test-users" % self.application_id
        return User(**self.graph.post(url, **parameters))

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
