import pytest

from eidos_sdk.agent.doc_manager.parsers.base_parser import BaseParserSpec, DataBlob
from eidos_sdk.agent.doc_manager.parsers.text_parsers import TextParser
from eidos_sdk.agent.doc_manager.transformer.text_splitters import RecursiveCharacterTextSplitter, RecursiveCharacterTextSplitterSpec


class TestRecursiveCharacterTextSplitter:
    @pytest.fixture()
    def small_data(self):
        data = "1234567890"
        return TextParser(BaseParserSpec()).parse(DataBlob(path="path/file.txt", mimetype="text/plain", data=data))

    @pytest.fixture()
    def large_data(self):
        data = (("1234567890 " * 10) + "\n") * 100
        return TextParser(BaseParserSpec()).parse(DataBlob(path="path/file.txt", mimetype="text/plain", data=data))

    @pytest.fixture()
    def splitter(self):
        return RecursiveCharacterTextSplitter(RecursiveCharacterTextSplitterSpec(chunk_size=220))

    def test_transform_documents_small_text(self, small_data, splitter):
        split_docs = list(splitter.transform_documents(small_data))
        assert len(split_docs) == 1
        doc = split_docs[0]
        assert doc.page_content == "1234567890"
        assert doc.metadata["source"] == "path/file.txt"
        assert doc.metadata["mime_type"] == "text/plain"

    def test_transform_documents_large_text(self, large_data, splitter):
        split_docs = list(splitter.transform_documents(large_data))
        assert len(split_docs) == 100
        doc = split_docs[0]
        assert doc.page_content == '1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890'
        assert doc.metadata["source"] == "path/file.txt"
        assert doc.metadata["mime_type"] == "text/plain"
