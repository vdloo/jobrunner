from flows.builtin.webserver.factory import simple_http_server_flow_factory
from flows.builtin.webserver.post import run_webserver
from tests.testcase import TestCase


class TestRunWebserver(TestCase):
    def setUp(self):
        self.post_job = self.set_up_patch(
            'flows.builtin.webserver.post.post_job'
        )

    def test_run_webserver_posts_job(self):
        run_webserver()

        expected_store = {
            'port': 8080
        }
        self.post_job.assert_called_once_with(
            simple_http_server_flow_factory,
            store=expected_store,
            capabilities={'port_is_free'}
        )

    def test_run_webserver_posts_job_with_specified_port(self):
        run_webserver(port=1234)

        expected_store = {
            'port': 1234
        }
        self.post_job.assert_called_once_with(
            simple_http_server_flow_factory,
            store=expected_store,
            capabilities={'port_is_free'}
        )
