import logging

from django.urls import reverse
from requests_oauthlib import OAuth2Session

logger = logging.getLogger(__file__)


class LinkedinLoginService:
    KEY = 'linkedin'

    SCOPE = ['profile', 'email', 'openid']
    AUTHORIZATION_BASE_URL = 'https://www.linkedin.com/oauth/v2/authorization'

    TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
    CLIENT_ID = None
    CLIENT_SECRET = None

    request = None
    service: OAuth2Session = None
    token = None

    def __init__(self, request, client_id, client_secret):
        self.request = request
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.service = OAuth2Session(self.CLIENT_ID,
                                     scope=self.SCOPE,
                                     redirect_uri=self.redirect_uri)

    @property
    def redirect_uri(self):
        return self.request.build_absolute_uri(
            reverse('oauth-login-callback', kwargs=dict(backend=self.KEY)))

    def get_authorization_url(self) -> (None, None):
        return self.service.authorization_url(self.AUTHORIZATION_BASE_URL)

    def process_response(self, authorization_response):
        try:
            self.token = self.service.fetch_token(self.TOKEN_URL,
                                                  client_secret=self.CLIENT_SECRET,
                                                  include_client_id=True,
                                                  authorization_response=self.request.get_full_path())
        except Warning as exc:
            self.token = exc.token
            self.service.token = exc.token

    def get_user_info(self):
        response = self.service.get('https://api.linkedin.com/v2/userinfo')

        return response.json()
