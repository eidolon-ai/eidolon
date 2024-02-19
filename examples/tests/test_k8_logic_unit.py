from kubernetes.client import CoreV1Api

from eidolon_examples.k8_monitor.k8_logic_unit import K8LogicUnit, _limit_obj


def test_all_dry_run_are_properly_placed():
    api = CoreV1Api()
    functions = [(f, getattr(api, f)) for f in dir(api) if not f.startswith("_") and callable(getattr(api, f))]
    almost_safe = {name for name, f in functions if "dry_run" in f.__doc__}
    assert almost_safe.intersection(K8LogicUnit.dangerous_operations()) == set()
    assert almost_safe.intersection(K8LogicUnit.safe_operations()) == set()
    assert almost_safe == K8LogicUnit.safe_with_dry_run()


def test_foo():
    api = CoreV1Api()
    functions = [f for f in dir(api) if not f.startswith("_") and callable(getattr(api, f))]
    _safe_operations = {f for f in functions if f.startswith("list") or f.startswith("read") or f.startswith("get")}
    _safe_with_dry_run = {
        f
        for f in functions
        if f.startswith("patch")
        or f.startswith("patch")
        or f.startswith("create")
        or f.startswith("replace")
        or f.startswith("delete")
    }
    _dangerous_operations = set(functions) - K8LogicUnit.safe_operations() - _safe_with_dry_run
    assert _safe_operations == K8LogicUnit.safe_operations()
    assert _safe_with_dry_run == K8LogicUnit.safe_with_dry_run()
    assert _dangerous_operations == K8LogicUnit.dangerous_operations()


def test_limit_object_ending_on_dict():
    o = dict(a=[dict(c="asdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdā")])
    _limit_obj(o, 20)
    assert o == {"a": [{"c": "..."}]}


def test_limit_object_ending_on_list():
    o = dict(a=["asdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdāasdā"])
    _limit_obj(o, 20)
    assert o == {"a": ["..."]}
