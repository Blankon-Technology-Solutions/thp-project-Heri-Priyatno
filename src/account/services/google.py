from django.urls import reverse
from requests_oauthlib import OAuth2Session


class GoogleLoginService:
    KEY = 'google'
    SCOPE = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ]
    AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://www.googleapis.com/oauth2/v4/token"

    CLIENT_ID = None
    CLIENT_SECRET = None
    CLIENT_PROJECT_ID = None
    request = None
    service: OAuth2Session = None
    token = None

    def __init__(self, request, client_id, client_secret, client_project_id):
        self.request = request
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.CLIENT_PROJECT_ID = client_project_id
        self.service = OAuth2Session(self.CLIENT_ID,
                                     scope=self.SCOPE,
                                     redirect_uri=self.redirect_uri)

    @property
    def redirect_uri(self):
        return self.request.build_absolute_uri(
            reverse('oauth-login-callback', kwargs=dict(backend=self.KEY)))

    def get_authorization_url(self) -> (None, None):
        return self.service.authorization_url(self.AUTHORIZATION_BASE_URL,
                                              access_type="offline",
                                              prompt="select_account")

    def process_response(self, authorization_response):
        self.token = self.service.fetch_token(self.TOKEN_URL,
                                              client_secret=self.CLIENT_SECRET,
                                              authorization_response=self.request.get_full_path())
        return self.token

    def get_user_info(self):
        response = self.service.get('https://www.googleapis.com/oauth2/v1/userinfo')

        return response.json()
