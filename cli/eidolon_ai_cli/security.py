import html
import os
import webbrowser

from oauthlib.oauth2 import WebApplicationClient
from prompt_toolkit import HTML, print_formatted_text
from requests_oauthlib import OAuth2Session

from eidolon_ai_cli.auth_web_server import AuthWebserver


class OAuth2CLI:
    oauth2_code: str

    def __init__(self, client_id, client_secret, authorization_base_url, token_url, scope=None):
        os.environ.setdefault('OAUTHLIB_INSECURE_TRANSPORT', '1')
        os.environ.setdefault('OAUTHLIB_RELAX_TOKEN_SCOPE', '1')
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_base_url = authorization_base_url
        self.token_url = token_url
        self.scope = scope
        self.oauth = self._create_oauth_session()

    def _create_oauth_session(self):
        client = WebApplicationClient(self.client_id)
        return OAuth2Session(client=client, redirect_uri=None, scope=self.scope)

    def get_authorization_url(self):
        return self.oauth.authorization_url(self.authorization_base_url, audience=self.client_id)

    def fetch_token(self, authorization_response):
        return self.oauth.fetch_token(self.token_url, authorization_response=authorization_response,
                                      client_id=self.client_id, client_secret=self.client_secret)

    def get_token(self):
        server = AuthWebserver()
        server.start_local_server()
        self.oauth.redirect_uri = f'http://localhost:{server.port}/auth'
        auth_url, _ = self.get_authorization_url()

        print_formatted_text(HTML(f"<b>Opening browser to authorize: {html.escape(auth_url)}</b>"))
        webbrowser.open(auth_url, new=2)

        oauth2_code = server.wait_for_token()
        token = self.fetch_token(oauth2_code)

        return token["access_token"]


class GoogleOAuth2CLI(OAuth2CLI):
    def __init__(self, client_id, client_secret, scope=None):
        if scope is None:
            scope = ["openid", "profile", "email"]
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            authorization_base_url='https://accounts.google.com/o/oauth2/auth',
            token_url='https://accounts.google.com/o/oauth2/token',
            scope=scope
        )


class ADOAuth2CLI(OAuth2CLI):
    def __init__(self, client_id, tenant_id, client_secret, scope=None):
        if scope is None:
            scope = ["openid", "email"]
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            authorization_base_url=f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize',
            token_url=f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token',
            scope=scope
        )


class OktaOAuth2CLI(OAuth2CLI):
    def __init__(self, client_id, domain, client_secret, scope=None):
        if scope is None:
            scope = ["openid", "email"]
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            authorization_base_url=f'https://{domain}/oauth2/v1/authorize',
            token_url=f'https://{domain}/oauth2/v1/token',
            scope=scope
        )


class GitHubOAuth2CLI(OAuth2CLI):
    def __init__(self, client_id, client_secret, scope=None):
        if scope is None:
            scope = ["read:user", "user:email"]
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            authorization_base_url='https://github.com/login/oauth/authorize',
            token_url='https://github.com/login/oauth/access_token',
            scope=scope
        )


security_providers = {
    'google': {
        'help': "Enable security with the Google OAuth2 provider.",
        'impl': GoogleOAuth2CLI,
        "args": {
            'client_id': {
                "env_var": "GOOGLE_CLIENT_ID"
            },
            'client_secret': {
                "env_var": "GOOGLE_CLIENT_SECRET"
            }
        }
    },
    'ad': {
        'help': "Enable security with the Azure AD OAuth2 provider.",
        'impl': ADOAuth2CLI,
        "args": {
            'client_id': {
                "env_var": "AZURE_CLIENT_ID"
            },
            'tenant_id': {
                "env_var": "AZURE_TENANT_ID"
            },
            'client_secret': {
                "env_var": "AZURE_CLIENT_SECRET"
            }

        }
    },
    'okta': {
        'help': "Enable security with the Okta OAuth2 provider.",
        'impl': OktaOAuth2CLI,
        "args": {
            'client_id': {
                "env_var": "OKTA_CLIENT_ID"
            },
            'domain': {
                "env_var": "OKTA_DOMAIN"
            },
            'client_secret': {
                "env_var": "OKTA_CLIENT_SECRET"
            }

        }
    },
    'github': {
        'help': "Enable security with the GitHub OAuth2 provider.",
        'impl': GitHubOAuth2CLI,
        "args": {
            'client_id': {
                "env_var": "GITHUB_CLIENT_ID"
            },
            'client_secret': {
                "env_var": "GITHUB_CLIENT_SECRET"
            }

        }
    }
}
