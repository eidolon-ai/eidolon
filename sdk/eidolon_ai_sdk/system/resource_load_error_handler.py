from eidolon_ai_client.util.logger import logger

fail_on_agent_start_error: bool = ...  # noqa: F821


def register_load_error(file_loc: str, e: Exception):
    logger.exception(f"Error loading resource {file_loc}", e)
    if fail_on_agent_start_error:
        raise e


def register_instantiate_error(name: str, resourceKind: str, e: Exception):
    logger.exception(f"Error instantiating resource {name} of kind {resourceKind}", e)
    if fail_on_agent_start_error:
        raise e


def register_agent_start_error(agentName: str, e: Exception):
    logger.exception(f"Error starting agent {agentName}", e)
    if fail_on_agent_start_error:
        raise e


def register_resource_error(resourceName: str, resourceKind: str, e: Exception):
    logger.exception(f"Error registering resource {resourceKind}.{resourceName}", e)
    if fail_on_agent_start_error:
        raise e


def register_resource_promote_error(name: str, resourceKind: str, kind, e: Exception):
    logger.exception(f"Error promoting resource {name} of kind {resourceKind} to {kind}", e)
    if fail_on_agent_start_error:
        raise e
