from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import DocumentLoader
from eidolon_ai_sdk.agent.doc_manager.loaders.memorywrapper_loader import WrappedMemoryLoader, WrappedMemoryLoaderSpec
from eidolon_ai_sdk.memory.azure_file_memory import AzureFileMemorySpec, AzureFileMemory
from eidolon_ai_sdk.system.specable import Specable
from eidolon_ai_sdk.util.class_utils import fqn


class AzureLoaderSpec(AzureFileMemorySpec):
    """
    Loads documents from an azure storage container.
    """

    pattern: str = "**"


class AzureLoader(DocumentLoader, Specable[AzureLoaderSpec]):
    loader: WrappedMemoryLoader

    def __init__(self, **kwargs: object):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self.loader = WrappedMemoryLoader(
            spec=WrappedMemoryLoaderSpec(
                memory=dict(
                    implementation=fqn(AzureFileMemory),
                    **self.spec.model_dump(),
                ),
                pattern=self.spec.pattern,
            )
        )

    def get_changes(self, *args, **kwargs):
        return self.loader.get_changes(*args, **kwargs)

    def list_files(self, *args, **kwargs):
        return self.loader.list_files(*args, **kwargs)
