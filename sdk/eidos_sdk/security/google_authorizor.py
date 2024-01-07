from typing import List

import httpx
import os
from pydantic import BaseModel, Field

from eidos_sdk.security.jwt_middleware import BaseJWTMiddleware
from eidos_sdk.system.reference_model import Specable


class GoogleJWTMiddlewareSpec(BaseModel):
    jwks_url: str = Field("https://www.googleapis.com/oauth2/v3/certs", description="The URL to fetch the JWKS from. Defaults to https://www.googleapis.com/oauth2/v3/certs")
    audience: str = Field(os.environ.get("GOOGLE_CLIENT_ID"), description="Your google client ID. Defaults to the environment variable GOOGLE_CLIENT_ID")
    issuer: str = Field(default="https://accounts.google.com", description="The issuer of the JWT. Defaults to https://accounts.google.com")


class GoogleJWTMiddleware(BaseJWTMiddleware, Specable[GoogleJWTMiddlewareSpec]):

    async def get_signing_keys(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(self.spec.jwks_url)
            return resp.json()["keys"]

    async def get_audience_and_issuer(self):
        return self.spec.audience, self.spec.issuer

    def get_algorithms(self) -> List[str]:
        return ["RS256"]
