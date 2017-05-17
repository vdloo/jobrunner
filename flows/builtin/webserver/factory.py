from taskflow.patterns import linear_flow as lf
from taskflow.retry import Times

from flows.builtin.webserver.tasks import SimpleHTTPServer


def simple_http_server_flow_factory():
    f = lf.Flow("simple_http_server_flow", retry=Times(10))
    f.add(
        SimpleHTTPServer(
            "run_simple_webserver"
        )
    )
    return f
