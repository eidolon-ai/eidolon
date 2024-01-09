from authlib.integrations.starlette_client import OAuth
from pydantic import BaseModel, Field
from starlette.config import Config
from typing import List, Optional

from abc import ABC, abstractmethod
from fastapi import Request, Response, FastAPI
from jose import jwt, JWTError
from starlette.responses import JSONResponse

from eidos_sdk.security.security_manager import BaseTokenProcessor
from eidos_sdk.system.reference_model import Specable
from eidos_sdk.system.request_context import RequestContext


class BaseJWTMiddlewareSpec(BaseModel):
    register_login_route: bool = Field(default=True, description="Whether or not to register the login route. Defaults to True")


class BaseJWTMiddleware(BaseTokenProcessor, ABC, Specable[BaseJWTMiddlewareSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_login_route = self.spec.register_login_route

    def start(self, app: FastAPI):
        if self.register_login_route:
            self.add_login_route(app)

    def add_login_route(self, app: FastAPI):
        config = self.getOAuthConfig()
        starlette_config = Config(environ=config)
        oauth = OAuth(starlette_config)
        self.register_auth(oauth)



    @abstractmethod
    def getOAuthConfig(self) -> dict:
        pass

    @abstractmethod
    def register_auth(self, oauth: OAuth):
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

    async def dispatch(self, request: Request) -> Optional[Response]:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(status_code=401, content={"detail": "Authorization header missing"})

        token = auth_header.split(" ")[1]
        try:
            jwks = await self.get_signing_keys()
            audience, issuer = await self.get_audience_and_issuer()
            payload = jwt.decode(token, jwks, algorithms=self.get_algorithms(), audience=audience, issuer=issuer)
            request.state.payload = payload

            RequestContext.set('Authorization', auth_header, propagate=True)
            RequestContext.set('jwt', payload)
            return None
        except JWTError as e:
            return JSONResponse(status_code=401, content={"detail": str(e)})
