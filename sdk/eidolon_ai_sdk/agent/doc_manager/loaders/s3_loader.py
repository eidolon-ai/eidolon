from typing import Optional

from pydantic import BaseModel, Field

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import DocumentLoader
from eidolon_ai_sdk.agent.doc_manager.loaders.memorywrapper_loader import WrappedMemoryLoader, WrappedMemoryLoaderSpec
from eidolon_ai_sdk.memory.s3_file_memory import S3FileMemory
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.class_utils import fqn


class S3LoaderSpec(BaseModel):
    """
    Loads documents from an S3 bucket.
    """

    bucket: str
    region_name: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None
    session_args: dict = Field({}, description="Additional arguments to pass to the boto3 session.")
    pattern: str = "**"


class S3Loader(DocumentLoader, Specable[S3LoaderSpec]):
    loader: WrappedMemoryLoader

    def __init__(self, **kwargs: object):
        super().__init__(**kwargs)
        self.loader = WrappedMemoryLoader(spec=WrappedMemoryLoaderSpec(
            memory=dict(
                implementation=fqn(S3FileMemory),
                **self.spec.model_dump(),
            ),
            pattern=self.spec.pattern,
        ))

    def get_changes(self, *args, **kwargs):
        return self.loader.get_changes(*args, **kwargs)

    def list_files(self, *args, **kwargs):
        return self.loader.list_files(*args, **kwargs)