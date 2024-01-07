from oauthlib.oauth2 import MobileApplicationClient
from requests_oauthlib import OAuth2Session


class OAuth2CLI:
    def __init__(self, client_id, authorization_base_url, token_url, scope=None, redirect_uri='urn:ietf:wg:oauth:2.0:oob'):
        self.client_id = client_id
        self.authorization_base_url = authorization_base_url
        self.token_url = token_url
        self.scope = scope
        self.redirect_uri = redirect_uri
        self.oauth = self._create_oauth_session()

    def _create_oauth_session(self):
        client = MobileApplicationClient(self.client_id)
        return OAuth2Session(client=client, redirect_uri=self.redirect_uri, scope=self.scope)

    def get_authorization_url(self):
        return self.oauth.authorization_url(self.authorization_base_url)

    def fetch_token(self, authorization_response):
        return self.oauth.fetch_token(self.token_url, authorization_response=authorization_response, client_id=self.client_id)


class GoogleOAuth2CLI(OAuth2CLI):
    def __init__(self, client_id, scope=None):
        super().__init__(
            client_id=client_id,
            authorization_base_url='https://accounts.google.com/o/oauth2/auth',
            token_url='https://accounts.google.com/o/oauth2/token',
            scope=scope
        )


class ADOAuth2CLI(OAuth2CLI):
    def __init__(self, client_id, tenant_id, scope=None):
        super().__init__(
            client_id=client_id,
            authorization_base_url=f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize',
            token_url=f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token',
            scope=scope
        )


class OktaOAuth2CLI(OAuth2CLI):
    def __init__(self, client_id, domain, scope=None):
        super().__init__(
            client_id=client_id,
            authorization_base_url=f'https://{domain}/oauth2/v1/authorize',
            token_url=f'https://{domain}/oauth2/v1/token',
            scope=scope
        )


class GitHubOAuth2CLI(OAuth2CLI):
    def __init__(self, client_id, scope=None):
        super().__init__(
            client_id=client_id,
            authorization_base_url='https://github.com/login/oauth/authorize',
            token_url='https://github.com/login/oauth/access_token',
            scope=scope
        )
