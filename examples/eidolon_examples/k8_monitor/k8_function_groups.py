from kubernetes.client import CoreV1Api

_operations = [
    (f, getattr(CoreV1Api, f)) for f in dir(CoreV1Api) if not f.startswith("_") and callable(getattr(CoreV1Api, f))
]

safe_operations = {o for o, f in _operations if o.startswith("list") or o.startswith("read") or o.startswith("get")}
safe_with_dry_run = {
    o
    for o, f in _operations
    if o.startswith("create") or o.startswith("replace") or o.startswith("patch") or o.startswith("delete")
}
dangerous_operations = {o for o, f in _operations if o.startswith("connect")}
