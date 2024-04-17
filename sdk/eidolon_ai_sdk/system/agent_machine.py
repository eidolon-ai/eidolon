import typing
from contextlib import contextmanager
from typing import List, Optional, Annotated, Literal, cast

from fastapi import FastAPI, Request, Body, Header
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse, Response

from eidolon_ai_client.client import ProcessStatus
from eidolon_ai_client.events import FileHandle
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent_os_interfaces import FileMemory, SymbolicMemory, SimilarityMemory, SecurityManager
from eidolon_ai_sdk.memory.agent_memory import AgentMemory
from .agent_contract import StateSummary, CreateProcessArgs, DeleteProcessResponse, ListProcessesResponse
from .agent_controller import AgentController
from .process_file_system import ProcessFileSystem
from .processes import ProcessDoc
from .reference_model import AnnotatedReference, Specable
from .resources.agent_resource import AgentResource
from .resources.resources_base import Resource
from ..agent_os import AgentOS
from ..cpu.agent_call_history import AgentCallHistory
from ..security.permissions import PermissionException


class MachineSpec(BaseModel):
    symbolic_memory: AnnotatedReference[SymbolicMemory] = Field(description="The Symbolic Memory implementation.")
    file_memory: AnnotatedReference[FileMemory] = Field(desciption="The File Memory implementation.")
    similarity_memory: AnnotatedReference[SimilarityMemory] = Field(description="The Vector Memory implementation.")
    security_manager: AnnotatedReference[SecurityManager] = Field(description="The Security Manager implementation.")
    process_file_system: AnnotatedReference[ProcessFileSystem] = Field(
        description="The Process File System implementation. Used to store files related to processes."
    )

    def get_agent_memory(self):
        file_memory = self.file_memory.instantiate()
        symbolic_memory = self.symbolic_memory.instantiate()
        vector_memory = self.similarity_memory.instantiate()
        return AgentMemory(
            file_memory=file_memory,
            symbolic_memory=symbolic_memory,
            similarity_memory=vector_memory,
        )


class AgentMachine(Specable[MachineSpec]):
    memory: AgentMemory
    security_manager: SecurityManager
    agent_controllers: List[AgentController]
    app: Optional[FastAPI]
    process_file_system: ProcessFileSystem

    def __init__(self, spec: MachineSpec):
        super().__init__(spec)
        self.memory = self.spec.get_agent_memory()
        agents = {}
        for name, r in AgentOS.get_resources(AgentResource).items():
            with _error_wrapper(r):
                agents[name] = r.spec.instantiate()
        self.memory = self.spec.get_agent_memory()
        self.agent_controllers = [AgentController(name, agent) for name, agent in agents.items()]
        self.app = None
        self.security_manager = self.spec.security_manager.instantiate()
        self.process_file_system = self.spec.process_file_system.instantiate()

    async def start(self, app):
        if self.app:
            raise Exception("Machine already started")

        app.add_api_route(
            "/processes",
            endpoint=self.list_processes,
            methods=["GET"],
            response_model=typing.List[dict],
            tags=["processes"],
        )

        app.add_api_route(
            "/processes/{process_id}",
            endpoint=self.get_process,
            methods=["GET"],
            response_model=ProcessStatus,
            tags=["processes"],
        )

        app.add_api_route(
            "/processes",
            endpoint=self.create_process,
            methods=["POST"],
            response_model=StateSummary,
            tags=["processes"],
        )

        app.add_api_route(
            "/processes/{process_id}",
            endpoint=self._delete_process,
            methods=["DELETE"],
            response_model=DeleteProcessResponse,
            tags=["processes"],
        )

        app.add_api_route(
            "/processes/{process_id}/events",
            endpoint=self.get_process_events,
            methods=["GET"],
            response_model=typing.List[typing.Dict[str, typing.Any]],
            tags=["processes"],
        )

        # Add routes for the process filesystem
        app.add_api_route(
            "/processes/{process_id}/files",
            endpoint=self.upload_file,
            methods=["POST"],
            response_model=FileHandle,
            tags=["files"],
        )

        app.add_api_route(
            "/processes/{process_id}/files/{file_id}",
            endpoint=self.download_file,
            methods=["GET"],
            response_model=bytes,
            tags=["files"],
        )

        app.add_api_route(
            "/processes/{process_id}/files/{file_id}/metadata",
            endpoint=self.set_metadata,
            methods=["POST"],
            response_model=FileHandle,
            tags=["files"],
        )

        app.add_api_route(
            "/processes/{process_id}/files/{file_id}",
            endpoint=self._delete_file,
            methods=["DELETE"],
            response_model=None,
            tags=["files"],
        )

        # Add the routes for the agent controllers
        for program in self.agent_controllers:
            await program.start(app)
        await self.memory.start()
        self.app = app

    async def stop(self):
        if self.app:
            for program in self.agent_controllers:
                await program.stop(self.app)
            await self.memory.stop()
            self.app = None

    def _get_agent_controller(self, agent_name: str) -> Optional[AgentController]:
        for controller in self.agent_controllers:
            if controller.name == agent_name:
                return controller
        return None

    async def upload_file(
        self,
        process_id: str,
        mime_type: Annotated[str | None, Header()] = None,
        file_bytes=Body(
            description="A byte stream that represents the file to be uploaded", media_type="application/octet-stream"
        ),
    ):
        """
        Upload a file for this process
        :param process_id:
        :param file_bytes:
        :return: The file id that was written
        """
        file_md = None
        if mime_type:
            file_md = {"mime_type": mime_type}
        file_id = await self.process_file_system.write_file(process_id, file_bytes, file_md)
        return JSONResponse(content=file_id.model_dump(), status_code=200)

    async def set_metadata(self, process_id: str, file_id: str, file_md: dict):
        """
        Set metadata for a file
        :param file_id:
        :param process_id:
        """
        file_id = await self.process_file_system.set_metadata(process_id, file_id, file_md)
        return JSONResponse(content=file_id.model_dump(), status_code=200)

    async def download_file(self, process_id: str, file_id: str):
        """
        Download a file for this process
        :param process_id:
        :param file_id:
        :return: The file bytes
        """
        file = await self.process_file_system.read_file(process_id, file_id)
        if not file:
            return JSONResponse(content={"detail": "File Not Found"}, status_code=404)
        headers = {
            "Content-Type": "application/octet-stream",
        }
        contents, metadata = file
        if metadata and "mimetype" in metadata:
            headers["mime-type"] = metadata["mimetype"]
            headers["Content-Type"] = metadata["mimetype"]
        return Response(content=contents, headers=headers, status_code=200)

    async def _delete_file(self, process_id: str, file_id: str):
        """
        Delete a file for this process
        :param process_id:
        :param file_id:
        :return:
        """
        response = await self.process_file_system.delete_file(process_id, file_id)
        if not response:
            return JSONResponse(content={"detail": "File Not Found"}, status_code=404)
        return JSONResponse(content=response, status_code=200)

    async def list_processes(
        self,
        request: Request,
        skip: int = 0,
        limit: Annotated[int, Field(ge=1, le=100)] = 100,
        sort: Literal["ascending", "descending"] = "ascending",
    ):
        """
        List all processes. Supports paging and sorting
        """
        security: SecurityManager = AgentOS.security_manager
        child_pids = await AgentCallHistory.get_child_pids()
        processes_acc = []
        async for process_ in ProcessDoc.find(
            query={}, projection={"data": 0}, sort=dict(updated=1 if sort == "ascending" else -1)
        ):
            process_ = cast(ProcessDoc, process_)
            try:
                await security.check_permissions("read", process_.agent, process_.record_id)
                if skip > 0:
                    skip -= 1
                else:
                    controller = self._get_agent_controller(process_.agent)
                    if not controller:
                        logger.error(
                            f"Could not find agent {process_.agent}, in {self.agent_controllers}, skipping process"
                        )
                    else:
                        summary = StateSummary(
                            agent=process_.agent,
                            process_id=process_.record_id,
                            state=process_.state,
                            available_actions=controller.get_available_actions(process_.state),
                            title=process_.title,
                            created=process_.created,
                            updated=process_.updated,
                        )
                        if summary.process_id in child_pids:
                            summary.parent_process_id = child_pids[summary.process_id]
                        processes_acc.append(summary)
            except PermissionException:
                logger.debug(f"Skipping process {process_.record_id} due to lack of permissions")

            if len(processes_acc) >= limit:
                break

        next_page_url = f"{request.url}/processes/?limit={limit}&skip={skip + limit}"
        return JSONResponse(
            ListProcessesResponse(
                total=len(processes_acc),
                processes=processes_acc,
                next=next_page_url,
            ).model_dump(),
            200,
        )

    async def get_process(self, process_id: str):
        process_doc: ProcessDoc = await ProcessDoc.find_one(query={"_id": process_id})
        if not process_doc:
            logger.info(f"Process {process_id} does not exist")
            return JSONResponse(content={"detail": "Process Not Found"}, status_code=404)
        else:
            child_pids = await AgentCallHistory.get_child_pids()
            security: SecurityManager = AgentOS.security_manager
            await security.check_permissions("read", process_doc.agent, process_id)
            process_ = cast(ProcessDoc, process_doc)
            controller = self._get_agent_controller(process_doc.agent)
            available_actions = []
            if controller:
                available_actions = controller.get_available_actions(process_doc.state)

            summary = StateSummary(
                agent=process_.agent,
                process_id=process_.record_id,
                state=process_.state,
                available_actions=available_actions,
                title=process_.title,
                created=process_.created,
                updated=process_.updated,
            )
            if summary.process_id in child_pids:
                summary.parent_process_id = child_pids[summary.process_id]
            return JSONResponse(content=summary.model_dump(), status_code=200)

    async def create_process(self, args: CreateProcessArgs):
        """
        Create a new process. Use this method first to get a process id before calling any other action
        :param args: An optional title for the process
        :return:
        """
        controller = self._get_agent_controller(args.agent)
        if not controller:
            logger.info(f"Agent {args.agent} does not exist")
            return JSONResponse(content={"detail": "Agent not found"}, status_code=404)
        return await controller.create_process(args.title)

    async def _delete_process(self, process_id: str):
        """
        Delete a process and all of its children
        """
        process_doc: ProcessDoc = await ProcessDoc.find_one(query={"_id": process_id})
        if not process_doc:
            logger.info(f"Process {process_id} does not exist")
            return JSONResponse(content={"detail": "Process Not Found"}, status_code=404)

        controller = self._get_agent_controller(process_doc.agent)
        if not controller:
            logger.info(f"Agent {process_doc.agent} does not exist")
            return JSONResponse(content={"detail": "Agent not found"}, status_code=404)
        return await controller.delete_process(process_id)

    async def get_process_events(self, process_id: str):
        """
        Delete a process and all of its children
        """
        process_doc: ProcessDoc = await ProcessDoc.find_one(query={"_id": process_id})
        if not process_doc:
            logger.info(f"Process {process_id} does not exist")
            return JSONResponse(content={"detail": "Process Not Found"}, status_code=404)

        controller = self._get_agent_controller(process_doc.agent)
        if not controller:
            logger.info(f"Agent {process_doc.agent} does not exist")
            return JSONResponse(content={"detail": "Agent not found"}, status_code=404)
        return await controller.get_process_events(process_id)


@contextmanager
def error_logger(filename: str = None):
    try:
        yield
    except Exception as e:
        raise ValueError(f"Error building resource {filename}") from e


def _error_wrapper(resource: Resource):
    return error_logger(AgentOS.get_resource_source(resource.kind, resource.metadata.name))
