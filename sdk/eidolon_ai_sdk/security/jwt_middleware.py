from abc import ABC, abstractmethod
from fastapi import Request, Response, FastAPI, HTTPException
from authlib.jose import jwt, JoseError

# noinspection PyPackageRequirements
from pydantic import BaseModel
from starlette.responses import JSONResponse
from typing import List, Optional, Any

from eidolon_ai_sdk.security.security_manager import BaseTokenProcessor
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_client.util.request_context import RequestContext


class BaseJWTProcessorSpec(BaseModel):
    pass


class BaseJWTProcessor(BaseTokenProcessor, ABC, Specable[BaseJWTProcessorSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def start(self, app: FastAPI):
        pass

    @abstractmethod
    async def get_signing_keys(self):
        pass

    @abstractmethod
    async def get_audience_and_issuer(self) -> tuple[str, str]:
        pass

    @abstractmethod
    def get_algorithms(self) -> List[str]:
        pass

    async def process_token(self, token: str) -> Optional[Any]:
        jwks = await self.get_signing_keys()
        return jwt.decode(token, jwks)

    async def check_auth(self, request: Request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        token = auth_header[7:]

        try:
            userInfo = await self.process_token(token)
            RequestContext.set("Authorization", auth_header, propagate=True)
            RequestContext.set("jwt", userInfo)
        except JoseError as e:
            raise HTTPException(status_code=401, detail=str(e))
