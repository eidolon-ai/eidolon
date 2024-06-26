from typing import Optional, Iterable, Union

import numpy as np
from pymupdf import pymupdf

from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DocumentParser, DocumentParserSpec, DataBlob
from eidolon_ai_sdk.memory.document import Document
from eidolon_ai_sdk.system.reference_model import Specable

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


class PyPDFParser(DocumentParser, Specable[PyPDFParserSpec]):
    def __init__(self, spec: PyPDFParserSpec):
        super().__init__(spec)
        self.password = spec.password

    def parse(self, blob: DataBlob) -> Iterable[Document]:
        if isinstance(blob.data, bytes):
            pdf_reader = pymupdf.open(stream=blob.data)
        elif not blob.data and blob.path:
            pdf_reader = pymupdf.open(blob.path)
        else:
            with blob.as_bytes() as data:
                pdf_reader = pymupdf.open(stream=data.read())
        if self.password:
            pdf_reader.authenticate(self.password)
        yield from [
            Document(
                page_content=page.get_text(),
                metadata={"source": blob.path, "page": page_number, "mime_type": blob.mimetype},
            )
            for page_number, page in enumerate(pdf_reader.pages())
        ]
