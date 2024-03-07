import httpx

from eidolon_ai_sdk.security.jwt_processor import BaseJWTProcessor


class OKTAAuth(BaseJWTProcessor):
    OKTA_DOMAIN = "your_okta_domain"
    JWKS_URL = f"https://{OKTA_DOMAIN}/oauth2/default/v1/keys"
    AUDIENCE = "your_api_audience"
    ISSUER = f"https://{OKTA_DOMAIN}/oauth2/default"

    async def get_signing_keys(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(self.JWKS_URL)
            return resp.json()["keys"]
