from eidos_sdk.system.request_context import RequestContext


def test_set_and_get():
    RequestContext.set("foo", "FOO")
    assert RequestContext["foo"] == "FOO"


def test_set_and_get_propagate():
    RequestContext.set("foo", "FOO", propagate=True)
    assert RequestContext["foo"] == "FOO"


def test_headers_only_show_propagated():
    RequestContext.set("foo", "FOO")
    RequestContext.set("bar", "BAR", propagate=True)
    assert RequestContext.headers == {"bar": "BAR", "X-Eidos-Context": "bar"}
