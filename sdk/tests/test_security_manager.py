from eidolon_ai_sdk.security.security_manager import SecurityManagerSpec


def test_security_manager_spec():
    spec = SecurityManagerSpec()
    assert type(spec.safe_paths) == set
    assert len(spec.safe_paths) >= 4
