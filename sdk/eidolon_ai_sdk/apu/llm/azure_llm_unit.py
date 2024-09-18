import os
from typing import Optional, List

from pydantic import Field

from eidolon_ai_sdk.apu.llm.open_ai_connection_handler import AzureOpenAIConnectionHandlerSpec, AzureOpenAIConnectionHandler, get_default_token_provider
from eidolon_ai_sdk.apu.llm.open_ai_llm_unit import OpenAILLMBaseSpec, OpenAILLMBase
from eidolon_ai_sdk.apu.llm_unit import LLMModel
from eidolon_ai_sdk.system.reference_model import Specable, Reference


class AzureLLMSpec(OpenAILLMBaseSpec):
    base_url: str = Field(description="The base URL for the Azure LLM API. ie, \"https://eidolon-azure.openai.azure.com/openai\"")
    model: Reference[LLMModel] = Field(
        description="The model to use for the LLM. Since Azure deployments use custom names, no default is provided. See https://www.eidolonai.com/docs/howto/swap_llm for more details. on defining custom models."
    )
    azure_ad_token_provider: Optional[Reference] = Field(default_factory=get_default_token_provider)
    token_provider_scopes: List[str] = ["https://cognitiveservices.azure.com/.default"]
    api_version: str = os.environ.get("OPENAI_API_VERSION") or "2024-02-01"
    client_args: dict = {}


class AzureLLMUnit(OpenAILLMBase, Specable[AzureLLMSpec]):
    def __init__(self, **kwargs):
        Specable.__init__(self, **kwargs)
        connection_handler = AzureOpenAIConnectionHandler(spec=AzureOpenAIConnectionHandlerSpec(
            azure_ad_token_provider=self.spec.azure_ad_token_provider,
            token_provider_scopes=self.spec.token_provider_scopes,
            api_version=self.spec.api_version,
            base_url=self.spec.base_url,
            **self.spec.client_args
        ))
        super().__init__(connection_handler=connection_handler, ** kwargs)
