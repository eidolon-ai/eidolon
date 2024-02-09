from kubernetes.client import CoreV1Api

from eidolon_examples.k8_monitor.k8_function_groups import dangerous_operations, safe_operations, safe_with_dry_run


def test_all_dry_run_are_properly_placed():
    api = CoreV1Api()
    functions = [(f, getattr(api, f)) for f in dir(api) if not f.startswith("_") and callable(getattr(api, f))]
    almost_safe = {name for name, f in functions if "dry_run" in f.__doc__}
    assert almost_safe.intersection(dangerous_operations) == set()
    assert almost_safe.intersection(safe_operations) == set()
    assert almost_safe == safe_with_dry_run


def test_foo():
    api = CoreV1Api()
    functions = [f for f in dir(api) if not f.startswith("_") and callable(getattr(api, f))]
    _safe_operations = {f for f in functions if f.startswith("list") or f.startswith("read")}
    _safe_with_dry_run = {
        f
        for f in functions
        if f.startswith("patch")
        or f.startswith("patch")
        or f.startswith("create")
        or f.startswith("replace")
        or f.startswith("delete")
    }
    _dangerous_operations = set(functions) - safe_operations - _safe_with_dry_run
    assert _safe_operations == safe_operations
    assert _safe_with_dry_run == safe_with_dry_run
    assert _dangerous_operations == dangerous_operations
