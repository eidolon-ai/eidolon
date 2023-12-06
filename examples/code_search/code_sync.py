import hashlib
import logging
import uuid
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemMovedEvent

from eidos.memory.agent_memory import AgentMemory
from eidos.memory.parsers.base_parser import DataBlob
from eidos.memory.parsers.code_ast_parsers.programing_language_parser import LanguageParser, LanguageParserSpec
from eidos.memory.embeddings import OpenAIEmbedding, OpenAIEmbeddingSpec
from examples.code_search.file_system_watcher import FileSystemWatcher


def hash_file(file_path, chunk_size=8192):
    """
    Hash the contents of a file using SHA-256.

    :param file_path: Path to the file to be hashed.
    :param chunk_size: Size of each chunk to read. Default is 8192 bytes.
    :return: Hexadecimal string of the hash.
    """
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        chunk = file.read(chunk_size)
        while chunk:
            hasher.update(chunk)
            chunk = file.read(chunk_size)
    return hasher.hexdigest()


class CodeSync:
    def __init__(self, root_dir: str, agent_memory: AgentMemory):
        self.root_dir = Path(root_dir)
        self.agent_memory = agent_memory
        self.embedder = OpenAIEmbedding(OpenAIEmbeddingSpec())
        self.file_watcher = FileSystemWatcher(self.root_dir, self.on_file_change)
        self.logger = logging.getLogger("eidolon")

    def on_file_change(self, event: FileSystemEvent):
        if event.is_directory:
            return
        if event.event_type == "created":
            self.addFile(event.src_path)
        elif event.event_type == "deleted":
            self.removeFile(event.src_path)
        elif event.event_type == "modified":
            self.removeFile(event.src_path)
            self.addFile(event.src_path)
        elif event.event_type == "moved":
            # noinspection PyTypeChecker
            movedEvent: FileSystemMovedEvent = event
            self.removeFile(movedEvent.src_path)
            self.addFile(movedEvent.dest_path)

    async def sync_all(self):
        # get all hashes from symbolic memory
        hashes = {}
        async for file in self.agent_memory.symbolic_memory.find("code_sync", {}):
            hashes[file["file_path"]] = file["file_hash"]

        self.logger.info(f"Found {len(hashes)} files in symbolic memory")
        added = {}
        modified = {}
        # iterate over all python files in the root_dir
        for file in self.root_dir.glob('**/*.py'):
            # get the file path relavtive to the root_dir
            file_path = str(file.relative_to(self.root_dir))
            # create a hash of the file at file path
            file_hash = hash_file(file)
            # retrieve the file md5 from symbolic memory
            if file_path in hashes:
                # if the file exists in symbolic memory, check if the hashes are different
                if file_hash != hashes[file_path]:
                    modified[file_path] = file_hash
                # delete from hashes
                del hashes[file_path]
            else:
                added[file_path] = file_hash

        self.logger.info(f"Found {len(added)} new files")
        self.logger.info(f"Found {len(modified)} modified files")
        self.logger.info(f"Found {len(hashes)} deleted files")

        # delete all files that are left in hashes
        self.logger.info(f"Deleting {len(hashes)} files")
        for file_path in hashes:
            await self.removeFile(self.root_dir / file_path)

        # add all new files
        self.logger.info(f"Adding {len(added)} files")
        for file_path in added:
            await self.addFile(self.root_dir / file_path)

        # update all modified files
        self.logger.info(f"Updating {len(modified)} files")
        for file_path, file_hash in modified.items():
            await self.removeFile(self.root_dir / file_path)
            await self.addFile(self.root_dir / file_path)

        self.logger.info("Sync complete")

    async def addFile(self, file_path: Path):
        language_parser = LanguageParser(LanguageParserSpec(language="python"))
        docs = list(language_parser.parse(DataBlob.from_path(path=str(file_path))))
        for doc in docs:
            doc.id = str(uuid.uuid4())
        await self.agent_memory.similarity_memory.add("code_sync", docs, self.embedder)
        await self.agent_memory.symbolic_memory.insert("code_sync", [
            {
                "file_path": str(file_path.relative_to(self.root_dir)),
                "file_hash": hash_file(file_path),
                "doc_ids": [doc.id for doc in docs]
             }])

    async def removeFile(self, file_path: Path):
        # get the doc ids for the file
        relative_path = str(file_path.relative_to(self.root_dir))
        doc = await self.agent_memory.symbolic_memory.find_one("code_sync", {"file_path": relative_path})
        if doc:
            # remove the docs from similarity memory
            await self.agent_memory.similarity_memory.delete("code_sync", doc["doc_ids"])
            # remove the file from symbolic memory
            await self.agent_memory.symbolic_memory.delete("code_sync", {"file_path": relative_path})
