import httpx
import os
from authlib.integrations.requests_client import OAuth2Session
from pydantic import BaseModel, Field
from typing import List, Optional, Any

from eidolon_ai_sdk.security.jwt_processor import BaseJWTProcessor
from eidolon_ai_sdk.system.reference_model import Specable


class GoogleJWTProcessorSpec(BaseModel):
    jwks_url: str = Field(
        "https://www.googleapis.com/oauth2/v3/certs",
        description="The URL to fetch the JWKS from. Defaults to https://www.googleapis.com/oauth2/v3/certs",
    )
    audience: str = Field(
        os.environ.get("GOOGLE_CLIENT_ID"),
        description="Your google client ID. Defaults to the environment variable GOOGLE_CLIENT_ID",
    )
    issuer: str = Field(
        default="accounts.google.com", description="The issuer of the JWT. Defaults to accounts.google.com"
    )


class GoogleJWTProcessor(BaseJWTProcessor, Specable[GoogleJWTProcessorSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.signing_keys = None

    async def get_signing_keys(self):
        if not self.signing_keys:
            async with httpx.AsyncClient() as client:
                resp = await client.get(self.spec.jwks_url)
                self.signing_keys = resp.json()["keys"]
        return self.signing_keys

    async def get_audience_and_issuer(self):
        return self.spec.audience, self.spec.issuer

    def get_algorithms(self) -> List[str]:
        return ["RS256"]

    async def process_token(self, token: str) -> Optional[Any]:
        # need to call into google to exchange the token for a user info
        authlib_session = OAuth2Session(self.spec.audience, token={"access_token": token, "token_type": "Bearer"})
        response = authlib_session.get("https://openidconnect.googleapis.com/v1/userinfo")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching user info: {response.status_code} {response.text}")
