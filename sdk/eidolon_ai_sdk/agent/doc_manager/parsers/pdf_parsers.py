import time

import numpy as np
import pypdf
from typing import Optional, Iterable, Union

from opentelemetry import trace

from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DocumentParser, DocumentParserSpec, DataBlob
from eidolon_ai_sdk.memory.document import Document
from eidolon_ai_sdk.system.reference_model import Specable

tracer = trace.get_tracer(__name__)

_PDF_FILTER_WITH_LOSS = ["DCTDecode", "DCT", "JPXDecode"]
_PDF_FILTER_WITHOUT_LOSS = [
    "LZWDecode",
    "LZW",
    "FlateDecode",
    "Fl",
    "ASCII85Decode",
    "A85",
    "ASCIIHexDecode",
    "AHx",
    "RunLengthDecode",
    "RL",
    "CCITTFaxDecode",
    "CCF",
    "JBIG2Decode",
]


def extract_from_images_with_rapidocr(
    images: Iterable[Union[Iterable[np.ndarray], bytes]],
) -> str:
    """Extract text from images with RapidOCR.

    Args:
        images: Images to extract text from.

    Returns:
        Text extracted from images.

    Raises:
        ImportError: If `rapidocr-onnxruntime` package is not installed.
    """
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError:
        raise ImportError(
            "`rapidocr-onnxruntime` package not found, please install it with " "`pip install rapidocr-onnxruntime`"
        )
    ocr = RapidOCR()
    text = ""
    for img in images:
        result, _ = ocr(img)
        if result:
            result = [text[1] for text in result]
            text += "\n".join(result)
    return text


class PyPDFParserSpec(DocumentParserSpec):
    password: Optional[Union[str, bytes]] = None
    extract_images: bool = False


class PyPDFParser(DocumentParser, Specable[PyPDFParserSpec]):
    def __init__(self, spec: PyPDFParserSpec):
        super().__init__(spec)
        self.password = spec.password
        self.extract_images = spec.extract_images

    def parse(self, blob: DataBlob) -> Iterable[Document]:
        with tracer.start_as_current_span(name="as bytes"):
            as_bytes = blob.as_bytes()
        with as_bytes as pdf_file_obj:
            with tracer.start_as_current_span(name="parse"):
                pdf_reader = pypdf.PdfReader(pdf_file_obj, password=self.password)
            yield from [
                self._transform(blob, page, page_number)
                for page_number, page in enumerate(pdf_reader.pages)
            ]

    def _transform(self, blob, page, page_number):
        extracted = self._extract_images_from_page(page)
        with tracer.start_as_current_span(name="PyPDFParser: extract text"):
            text = page.extract_text()
        with tracer.start_as_current_span(name="PyPDFParser: transform"):
            return Document(
                page_content=text + extracted,
                metadata={"source": blob.path, "page": page_number, "mime_type": blob.mimetype},
            )

    # noinspection PyProtectedMember
    def _extract_images_from_page(self, page: pypdf._page.PageObject) -> str:
        with tracer.start_as_current_span(name="extract images"):
            # noinspection PyUnresolvedReferences
            if not self.extract_images or "/XObject" not in page["/Resources"].keys():
                return ""

            xObject = page["/Resources"]["/XObject"].get_object()  # type: ignore
            images = []
            for obj in xObject:
                if xObject[obj]["/Subtype"] == "/Image":
                    if xObject[obj]["/Filter"][1:] in _PDF_FILTER_WITHOUT_LOSS:
                        height, width = xObject[obj]["/Height"], xObject[obj]["/Width"]

                        images.append(np.frombuffer(xObject[obj].get_data(), dtype=np.uint8).reshape(height, width, -1))
                    elif xObject[obj]["/Filter"][1:] in _PDF_FILTER_WITH_LOSS:
                        images.append(xObject[obj].get_data())
                    else:
                        self.logger.warn("Unknown PDF Filter!")
            return extract_from_images_with_rapidocr(images)
