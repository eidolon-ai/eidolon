from typing import Dict, List

from eidolon_ai_client.util.logger import logger

fail_on_agent_start_error: bool = ...  # noqa: F821

load_errors: Dict[str, List[str]] = {}
start_errors: Dict[str, List[str]] = {}


def _add_load_error(name: str, error: str):
    if name not in load_errors:
        load_errors[name] = []
    load_errors[name].append(error)


def _add_start_error(name: str, error: str):
    if name not in load_errors:
        load_errors[name] = []
    start_errors[name].append(error)


def register_load_error(file_loc: str, e: Exception):
    logger.exception(f"Error loading resource {file_loc}", e)
    if fail_on_agent_start_error:
        raise e


def register_instantiate_error(name: str, resourceKind: str, e: Exception):
    logger.exception(f"Error instantiating resource {name} of kind {resourceKind}", e)
    _add_load_error(name, f"Error instantiating resource {name} of kind {resourceKind}: {e}")
    if fail_on_agent_start_error:
        raise e


def register_agent_start_error(agentName: str, e: Exception):
    logger.exception(f"Error starting agent {agentName}", e)
    _add_start_error(agentName, f"Error starting agent {agentName}: {e}")
    if fail_on_agent_start_error:
        raise e


def register_resource_error(resourceName: str, resourceKind: str, e: Exception):
    logger.exception(f"Error registering resource {resourceKind}.{resourceName}", e)
    _add_load_error(resourceName, f"Error registering resource {resourceName} of kind {resourceKind}: {e}")
    if fail_on_agent_start_error:
        raise e


def register_resource_promote_error(name: str, resourceKind: str, kind, e: Exception):
    logger.exception(f"Error promoting resource {name} of kind {resourceKind} to {kind}", e)
    _add_load_error(name, f"Error promoting resource {name} of kind {resourceKind}: {e}")
    if fail_on_agent_start_error:
        raise e
