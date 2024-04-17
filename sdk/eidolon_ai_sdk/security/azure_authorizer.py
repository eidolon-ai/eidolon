import os
from typing import List, Optional, Any

import httpx
from jose import jwt
from pydantic import BaseModel, Field

from eidolon_ai_sdk.security.jwt_processor import BaseJWTProcessor
from eidolon_ai_sdk.system.reference_model import Specable


class AzureJWTProcessorSpec(BaseModel):
    client_id: str = Field(
        os.environ.get("AZURE_CLIENT_ID") or os.environ.get("AZURE_AD_CLIENT_ID"),
        description="Your azure client or application ID. Defaults to the environment variable AZURE_CLIENT_ID",
    )
    tenant_id: str = Field(
        default=os.environ.get("AZURE_TENANT_ID") or os.environ.get("AZURE_AD_TENANT_ID"),
        description="The tenant id of the JWT. Defaults to the environment variable AZURE_TENANT_ID",
    )
    issuer_prefix: str = Field(
        default="https://sts.windows.net",
        description="The issuer prefix of the JWT. Defaults to sts.windows.net.  The tenant id will be appended to this value.  For example, sts.windows.net/your_tenant_id",
    )


class AzureJWTProcessor(BaseJWTProcessor, Specable[AzureJWTProcessorSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.signing_keys = None
        self.jwks_url = (
            f"https://login.microsoftonline.com/{self.spec.tenant_id}/discovery/keys?appid={self.spec.client_id}"
        )

    async def get_signing_keys(self):
        if not self.signing_keys:
            async with httpx.AsyncClient() as client:
                resp = await client.get(self.jwks_url)
                self.signing_keys = resp.json()["keys"]
        return self.signing_keys

    async def get_audience_and_issuer(self):
        return self.spec.client_id, self.spec.issuer_prefix + "/" + self.spec.tenant_id + "/"

    def get_algorithms(self) -> List[str]:
        return ["RS256"]

    async def process_token(self, token: str) -> Optional[Any]:
        jwks = await self.get_signing_keys()
        audience, issuer = await self.get_audience_and_issuer()
        token = jwt.decode(
            token=token, key=jwks, algorithms=self.get_algorithms(), audience=self.spec.client_id, issuer=issuer
        )
        return token
