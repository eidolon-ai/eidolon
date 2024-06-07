import os

from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidolon_ai_sdk.agent.doc_manager.parsers.pdf_parsers import PyPDFParser, PyPDFParserSpec


class TestPDFParser:
    def test_parse(self):
        data = DataBlob.from_path(os.path.dirname(os.path.abspath(__file__)) + "/AgentXOS.pdf")
        parser = PyPDFParser(PyPDFParserSpec())
        docs = list(parser.parse(data))
        assert docs
        doc = docs[0]
        assert doc.metadata["source"] == os.path.dirname(os.path.abspath(__file__)) + "/AgentXOS.pdf"
        assert doc.metadata["mime_type"] == "application/pdf"
        assert "What is an Agent?" in doc.page_content

    def test_parses_bytes(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + "/AgentXOS.pdf", "rb") as f:
            data = DataBlob.from_bytes(f.read(), path=None)
        parser = PyPDFParser(PyPDFParserSpec())
        docs = list(parser.parse(data))
        assert docs
        assert "What is an Agent?" in docs[0].page_content

    def test_parses_bytes_like(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + "/AgentXOS.pdf", "rb") as f:
            data = DataBlob(data=f, mimetype="application/pdf")
            parser = PyPDFParser(PyPDFParserSpec())
            docs = list(parser.parse(data))
            assert docs
        assert "What is an Agent?" in docs[0].page_content
