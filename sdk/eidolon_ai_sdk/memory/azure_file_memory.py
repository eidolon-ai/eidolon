import fnmatch
import os
from typing import AsyncIterable, Optional

from azure.identity.aio import EnvironmentCredential
from azure.storage.blob.aio import BlobServiceClient, ContainerClient
from pydantic import BaseModel, Field

from eidolon_ai_sdk.agent_os_interfaces import FileMetadata
from eidolon_ai_sdk.memory.file_memory import FileMemoryBase
from eidolon_ai_sdk.system.reference_model import Reference, Specable


def _get_default_token_provider():
    if os.environ.get("AZURE_CLIENT_ID") and os.environ.get("AZURE_CLIENT_SECRET") and os.environ.get("AZURE_TENANT_ID"):
        return Reference[EnvironmentCredential]()
    return None


class AzureFileMemorySpec(BaseModel):
    azure_ad_token_provider: Optional[Reference[object]] = Field(default_factory=_get_default_token_provider)
    account_url: str = Field(
        description="The URL of the Azure storage account of the form https://<OAUTH_STORAGE_ACCOUNT_NAME>.blob.core.windows.net."
    )
    container: str = Field(description="The name of the container to use.")
    create_container_on_startup: bool = Field(
        default=False, description="If true, the container will be created on startup if not already present."
    )


class AzureFileMemory(FileMemoryBase, Specable[AzureFileMemorySpec]):
    _client: BlobServiceClient = None
    _container: ContainerClient = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)

    async def _get_container(self):
        if not self._container:
            provider = None
            if self.spec.azure_ad_token_provider:
                provider = self.spec.azure_ad_token_provider.instantiate()
            self._client = BlobServiceClient(account_url=self.spec.account_url, credential=provider)
            self._container = self._client.get_container_client(self.spec.container)
            if self.spec.create_container_on_startup and not await self._container.exists():
                await self._container.create_container()

        return self._container

    async def start(self):
        pass

    async def stop(self):
        if self._client:
            await self._client.close()

    async def read_file(self, file_path: str) -> bytes:
        container = await self._get_container()
        blob = await container.download_blob(file_path)
        return await blob.readall()

    async def write_file(self, file_path: str, file_contents: bytes) -> None:
        container = await self._get_container()
        await container.upload_blob(file_path, file_contents, overwrite=True)

    async def delete_file(self, file_path: str) -> None:
        container = await self._get_container()
        await container.delete_blob(file_path)

    async def mkdir(self, directory: str, exist_ok: bool = False):
        pass

    async def exists(self, file_name: str):
        container = await self._get_container()
        return await container.get_blob_client(file_name).exists()

    async def glob(self, pattern: str) -> AsyncIterable[FileMetadata]:
        container = await self._get_container()
        async for blob in container.list_blobs(include="metadata"):
            if fnmatch.fnmatch(blob.name, pattern):
                yield FileMetadata(file_path=blob.name, hash=blob.etag, updated=blob.last_modified)
