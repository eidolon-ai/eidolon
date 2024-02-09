import kubernetes
from kubernetes.client import CoreV1Api
from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.io.events import StringOutputEvent, ObjectOutputEvent
from eidolon_ai_sdk.system.reference_model import Specable


functions = ['connect_delete_namespaced_pod_proxy', 'connect_delete_namespaced_pod_proxy_with_path', 'connect_delete_namespaced_service_proxy',
             'connect_delete_namespaced_service_proxy_with_path', 'connect_delete_node_proxy', 'connect_delete_node_proxy_with_path',
             'connect_get_namespaced_pod_attach', 'connect_get_namespaced_pod_exec', 'connect_get_namespaced_pod_portforward',
             'connect_get_namespaced_pod_proxy', 'connect_get_namespaced_pod_proxy_with_path', 'connect_get_namespaced_service_proxy',
             'connect_get_namespaced_service_proxy_with_path', 'connect_get_node_proxy', 'connect_get_node_proxy_with_path',
             'connect_head_namespaced_pod_proxy', 'connect_head_namespaced_pod_proxy_with_path', 'connect_head_namespaced_service_proxy',
             'connect_head_namespaced_service_proxy_with_path', 'connect_head_node_proxy', 'connect_head_node_proxy_with_path',
             'connect_options_namespaced_pod_proxy', 'connect_options_namespaced_pod_proxy_with_path', 'connect_options_namespaced_service_proxy',
             'connect_options_namespaced_service_proxy_with_path', 'connect_options_node_proxy', 'connect_options_node_proxy_with_path',
             'connect_patch_namespaced_pod_proxy', 'connect_patch_namespaced_pod_proxy_with_path', 'connect_patch_namespaced_service_proxy',
             'connect_patch_namespaced_service_proxy_with_path', 'connect_patch_node_proxy', 'connect_patch_node_proxy_with_path',
             'connect_post_namespaced_pod_attach', 'connect_post_namespaced_pod_exec', 'connect_post_namespaced_pod_portforward',
             'connect_post_namespaced_pod_proxy', 'connect_post_namespaced_pod_proxy_with_path', 'connect_post_namespaced_service_proxy',
             'connect_post_namespaced_service_proxy_with_path', 'connect_post_node_proxy', 'connect_post_node_proxy_with_path',
             'connect_put_namespaced_pod_proxy', 'connect_put_namespaced_pod_proxy_with_path', 'connect_put_namespaced_service_proxy',
             'connect_put_namespaced_service_proxy_with_path', 'connect_put_node_proxy', 'connect_put_node_proxy_with_path',
             'create_namespace', 'create_namespaced_binding', 'create_namespaced_config_map', 'create_namespaced_endpoints',
             'create_namespaced_event', 'create_namespaced_limit_range', 'create_namespaced_persistent_volume_claim', 'create_namespaced_pod',
             'create_namespaced_pod_binding', 'create_namespaced_pod_eviction', 'create_namespaced_pod_template', 'create_namespaced_replication_controller',
             'create_namespaced_resource_quota', 'create_namespaced_secret', 'create_namespaced_service', 'create_namespaced_service_account',
             'create_namespaced_service_account_token', 'create_node', 'create_persistent_volume', 'delete_collection_namespaced_config_map',
             'delete_collection_namespaced_endpoints', 'delete_collection_namespaced_event', 'delete_collection_namespaced_limit_range',
             'delete_collection_namespaced_persistent_volume_claim', 'delete_collection_namespaced_pod', 'delete_collection_namespaced_pod_template',
             'delete_collection_namespaced_replication_controller', 'delete_collection_namespaced_resource_quota', 'delete_collection_namespaced_secret',
             'delete_collection_namespaced_service', 'delete_collection_namespaced_service_account', 'delete_collection_node',
             'delete_collection_persistent_volume', 'delete_namespace', 'delete_namespaced_config_map', 'delete_namespaced_endpoints',
             'delete_namespaced_event', 'delete_namespaced_limit_range', 'delete_namespaced_persistent_volume_claim', 'delete_namespaced_pod',
             'delete_namespaced_pod_template', 'delete_namespaced_replication_controller', 'delete_namespaced_resource_quota',
             'delete_namespaced_secret', 'delete_namespaced_service', 'delete_namespaced_service_account', 'delete_node',
             'delete_persistent_volume', 'get_api_resources', 'list_component_status', 'list_config_map_for_all_namespaces',
             'list_endpoints_for_all_namespaces', 'list_event_for_all_namespaces', 'list_limit_range_for_all_namespaces', 'list_namespace',
             'list_namespaced_config_map', 'list_namespaced_endpoints', 'list_namespaced_event', 'list_namespaced_limit_range',
             'list_namespaced_persistent_volume_claim', 'list_namespaced_pod', 'list_namespaced_pod_template', 'list_namespaced_replication_controller',
             'list_namespaced_resource_quota', 'list_namespaced_secret', 'list_namespaced_service', 'list_namespaced_service_account',
             'list_node', 'list_persistent_volume', 'list_persistent_volume_claim_for_all_namespaces', 'list_pod_for_all_namespaces',
             'list_pod_template_for_all_namespaces', 'list_replication_controller_for_all_namespaces', 'list_resource_quota_for_all_namespaces',
             'list_secret_for_all_namespaces', 'list_service_account_for_all_namespaces', 'list_service_for_all_namespaces', 'patch_namespace',
             'patch_namespace_status', 'patch_namespaced_config_map', 'patch_namespaced_endpoints', 'patch_namespaced_event',
             'patch_namespaced_limit_range', 'patch_namespaced_persistent_volume_claim', 'patch_namespaced_persistent_volume_claim_status',
             'patch_namespaced_pod', 'patch_namespaced_pod_ephemeralcontainers', 'patch_namespaced_pod_status', 'patch_namespaced_pod_template',
             'patch_namespaced_replication_controller', 'patch_namespaced_replication_controller_scale', 'patch_namespaced_replication_controller_status',
             'patch_namespaced_resource_quota', 'patch_namespaced_resource_quota_status', 'patch_namespaced_secret', 'patch_namespaced_service',
             'patch_namespaced_service_account', 'patch_namespaced_service_status', 'patch_node', 'patch_node_status', 'patch_persistent_volume',
             'patch_persistent_volume_status', 'read_component_status', 'read_namespace', 'read_namespace_status', 'read_namespaced_config_map',
             'read_namespaced_endpoints', 'read_namespaced_event', 'read_namespaced_limit_range', 'read_namespaced_persistent_volume_claim',
             'read_namespaced_persistent_volume_claim_status', 'read_namespaced_pod', 'read_namespaced_pod_ephemeralcontainers',
             'read_namespaced_pod_log', 'read_namespaced_pod_status', 'read_namespaced_pod_template', 'read_namespaced_replication_controller',
             'read_namespaced_replication_controller_scale', 'read_namespaced_replication_controller_status', 'read_namespaced_resource_quota',
             'read_namespaced_resource_quota_status', 'read_namespaced_secret', 'read_namespaced_service', 'read_namespaced_service_account',
             'read_namespaced_service_status', 'read_node', 'read_node_status', 'read_persistent_volume', 'read_persistent_volume_status',
             'replace_namespace', 'replace_namespace_finalize', 'replace_namespace_status', 'replace_namespaced_config_map', 'replace_namespaced_endpoints',
             'replace_namespaced_event', 'replace_namespaced_limit_range', 'replace_namespaced_persistent_volume_claim',
             'replace_namespaced_persistent_volume_claim_status', 'replace_namespaced_pod', 'replace_namespaced_pod_ephemeralcontainers',
             'replace_namespaced_pod_status', 'replace_namespaced_pod_template', 'replace_namespaced_replication_controller',
             'replace_namespaced_replication_controller_scale', 'replace_namespaced_replication_controller_status', 'replace_namespaced_resource_quota',
             'replace_namespaced_resource_quota_status', 'replace_namespaced_secret', 'replace_namespaced_service',
             'replace_namespaced_service_account', 'replace_namespaced_service_status', 'replace_node', 'replace_node_status',
             'replace_persistent_volume', 'replace_persistent_volume_status']


class AgentsLogicUnitSpec(BaseModel):
    pass


class K8LogicUnit(Specable[AgentsLogicUnitSpec], LogicUnit):
    _client: CoreV1Api = None

    def client(self):
        if not self._client:
            kubernetes.config.load_kube_config()
            self._client = CoreV1Api()
        return self._client

    @llm_function()
    async def core_v1_api(self, function_name: str, kwargs: dict = None):
        """
        This function is a wrapper around kubernetes.client.CoreV1Api. It will call functions on the CoreV1Api object
        and return the results. For example, to list pods function_name would be "list_namespaced_pod" and kwargs may be
        {"namespace": "default", "limit": 20}

        impl: getattr(self.client(), function_name)(**kwargs)
        """
        kwargs = kwargs or {}
        if function_name.startswith("_"):
            raise ValueError(f"Private functions are not allowed")
        bad_keys = ["async_req", "watch"]
        for key in bad_keys:
            if key in kwargs:
                del kwargs[key]
        resp = getattr(self.client(), function_name)(**kwargs)
        try:
            yield ObjectOutputEvent(content=to_jsonable_python(resp))
        except Exception:
            yield StringOutputEvent(content=str(resp))

    # @llm_function()
    async def help(self, function_name: str):
        """
        This function is a wrapper around kubernetes.client.CoreV1Api. It will call functions on the CoreV1Api object
        and return the results.

        impl: getattr(self.client(), function_name).__doc__
        """
        return getattr(self.client(), function_name).__doc__

    # @llm_function()
    async def list_functions(self):
        """
        This function will list the functions that are available to be called on the CoreV1Api object.

        impl: dir(CoreV1Api)
        """
        return [f for f in dir(CoreV1Api) if not f.startswith("_")]


