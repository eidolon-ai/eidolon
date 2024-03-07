import os
from typing import List, Optional, Any

import httpx
from jose import jwt
from pydantic import BaseModel, Field

from eidolon_ai_sdk.security.jwt_processor import BaseJWTProcessor
from eidolon_ai_sdk.system.reference_model import Specable


class MSFTJWTProcessorSpec(BaseModel):
    jwks_url: str = Field(
        "https://login.microsoftonline.com/common/discovery/keys",
        description="The URL to fetch the JWKS from. Defaults to https://login.microsoftonline.com/common/discovery/keys",
    )
    audience: str = Field(
        os.environ.get("AZURE_AD_CLIENT_ID"),
        description="Your azure client or application ID. Defaults to the environment variable AZURE_AD_CLIENT_ID",
    )
    issuer_prefix: str = Field(
        default="sts.windows.net",
        description="The issuer prefix of the JWT. Defaults to sts.windows.net.  The tenant id will be appended to this value.  For example, sts.windows.net/your_tenant_id"
    )
    tenant_id: str = Field(
        default=os.environ.get("AZURE_AD_TENANT_ID"), description="The tenant id of the JWT. Defaults to the environment variable AZURE_AD_TENANT_ID"
    )


class MSFTJWTProcessor(BaseJWTProcessor, Specable[MSFTJWTProcessorSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.signing_keys = None
        self.jwks_url = f"https://login.microsoftonline.com/{self.spec.tenant_id}/discovery/keys?appid={self.spec.audience}"

    async def get_signing_keys(self):
        if not self.signing_keys:
            async with httpx.AsyncClient() as client:
                resp = await client.get(self.jwks_url)
                self.signing_keys = resp.json()["keys"]
        return self.signing_keys

    async def get_audience_and_issuer(self):
        return self.spec.audience, self.spec.issuer_prefix + "/" + self.spec.tenant_id

    def get_algorithms(self) -> List[str]:
        return ["RS256"]

    async def process_token(self, token: str) -> Optional[Any]:
        jwks = await self.get_signing_keys()

        issuer = f'https://login.microsoftonline.com/{self.spec.tenant_id.strip()}/v2.0'
        token = jwt.decode(token=token,
                           key=jwks,
                           algorithms=self.get_algorithms(),
                           audience=self.spec.audience,
                           issuer=issuer
                           )
        return token
