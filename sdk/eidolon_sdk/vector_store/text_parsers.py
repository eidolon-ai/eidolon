from typing import Iterable, Dict, Union

from bs4 import BeautifulSoup

from eidolon_sdk.reference_model import Specable
from eidolon_sdk.vector_store.base_parser import BaseParser, DataBlob, BaseParserSpec
from eidolon_sdk.vector_store.document import Document


class TextParser(BaseParser):
    def parse(self, blob: DataBlob) -> Iterable[Document]:
        yield Document(page_content=blob.as_string(), metadata={"source": blob.path})


class PyPDFParserSpec(BaseParserSpec):
    features: str = "lxml"
    text_separator: str = ""


class BS4HTMLParser(BaseParser, Specable[PyPDFParserSpec]):
    """Pparse HTML files using `Beautiful Soup`."""

    def __init__(self, spec: PyPDFParserSpec):
        super().__init__(spec)
        self.bs_kwargs = {"features": spec.features}
        self.text_separator = spec.text_separator

    def parse(self, blob: DataBlob) -> Iterable[Document]:
        with blob.as_bytes_io() as f:
            soup = BeautifulSoup(f, **self.bs_kwargs)

        text = soup.get_text(self.text_separator)

        if soup.title:
            title = str(soup.title.string)
        else:
            title = ""

        metadata: Dict[str, Union[str, None]] = {
            "source": blob.source,
            "title": title,
        }
        yield Document(page_content=text, metadata=metadata)

