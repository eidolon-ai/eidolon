import pytest

from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DataBlob, DocumentParserSpec
from eidolon_ai_sdk.agent.doc_manager.parsers.text_parsers import TextParser


class TestTextParser:
    @pytest.fixture()
    def text_parser(self):
        return TextParser(DocumentParserSpec())

    def test_parse_simple_string(self, text_parser: TextParser):
        data = DataBlob(path="path/file.txt", mimetype="text/plain", data="data")
        docs = list(text_parser.parse(data))
        assert len(docs) == 1
        doc = docs[0]
        assert doc.page_content == "data"
        assert doc.metadata["source"] == "path/file.txt"
        assert doc.metadata["mime_type"] == "text/plain"

    def test_parse_large_string(self, text_parser: TextParser):
        string = (("1234567890 " * 10) + "\n") * 100
        data = DataBlob(path="path/file.txt", mimetype="text/plain", data=string)
        docs = list(text_parser.parse(data))
        assert len(docs) == 1
        doc = docs[0]
        assert doc.page_content == string
        assert doc.metadata["source"] == "path/file.txt"
        assert doc.metadata["mime_type"] == "text/plain"
