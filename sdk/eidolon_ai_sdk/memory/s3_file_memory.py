import asyncio
import fnmatch
from io import BytesIO
from typing import AsyncIterable

import boto3
from pydantic import BaseModel

from eidolon_ai_sdk.agent_os_interfaces import FileMetadata
from eidolon_ai_sdk.memory.file_memory import FileMemoryBase
from eidolon_ai_sdk.util.async_wrapper import make_async


class S3FileMemory(BaseModel, FileMemoryBase):
    bucket: str
    region: str = "us-east-1"
    kwargs: dict = {}
    create_bucket_on_startup: bool = False
    _client = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @make_async
    def start(self):
        if self.create_bucket_on_startup:
            self.client().create()

    async def stop(self):
        pass

    def client(self):
        if not self._client:
            self._client = boto3.resource("s3", self.region, **self.kwargs).Bucket(self.bucket)
        return self._client

    @make_async
    def read_file(self, file_path: str) -> bytes:
        with BytesIO() as buffer:
            self.client().download_fileobj(file_path, buffer)
            buffer.seek(0)
            return buffer.read()

    @make_async
    def write_file(self, file_path: str, file_contents: bytes) -> None:
        with BytesIO() as buffer:
            buffer.write(file_contents)
            buffer.seek(0)
            self.client().upload_fileobj(buffer, file_path)

    @make_async
    def delete_file(self, file_path: str) -> None:
        self.client().delete_objects(Delete={"Objects": [{"Key": file_path}]})

    async def mkdir(self, directory: str, exist_ok: bool = False):
        pass

    @make_async
    def exists(self, file_name: str):
        for page in self.client().objects.filter(Prefix=file_name).pages():
            for object in page:
                if object.key == file_name:
                    return True
        return False

    async def glob(self, pattern: str) -> AsyncIterable[FileMetadata]:
        loop = asyncio.get_event_loop()
        pages = self.client().objects.pages()
        try:
            while True:
                page = await loop.run_in_executor(None, next, pages)
                for o in page:
                    if fnmatch.fnmatch(o.key, pattern):
                        yield FileMetadata(file_path=o.key, hash=o.e_tag, updated=o.last_modified)
        except StopIteration:
            pass
