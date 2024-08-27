import asyncio
import fnmatch
from io import BytesIO
from typing import AsyncIterable, Optional

import boto3
from pydantic import BaseModel, Field

from eidolon_ai_sdk.agent_os_interfaces import FileMetadata
from eidolon_ai_sdk.memory.file_memory import FileMemoryBase
from eidolon_ai_sdk.util.async_wrapper import make_async


class S3FileMemory(BaseModel, FileMemoryBase):
    bucket: str
    region_name: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None
    session_args: dict = Field({}, description="Additional arguments to pass to the boto3 session.")
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
            session = boto3.Session(
                region_name=self.region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_session_token=self.aws_session_token,
                **self.session_args,
            )
            self._client = session.resource("s3").Bucket(self.bucket)
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
            for o in page:
                if o.key == file_name:
                    return True
        return False

    async def glob(self, pattern: str) -> AsyncIterable[FileMetadata]:
        loop = asyncio.get_event_loop()
        pages = self.client().objects.pages()

        def get_next():
            try:
                return next(pages)
            except StopIteration:  # executor will not propagate stop iteration
                return None

        while True:
            page = await loop.run_in_executor(None, get_next)
            if page is None:  # explicit none check since page could potentially be empty
                break
            for o in page:
                if fnmatch.fnmatch(o.key, pattern):
                    yield FileMetadata(file_path=o.key, hash=o.e_tag, updated=o.last_modified)
