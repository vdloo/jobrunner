from flows.builtin.webserver.factory import simple_http_server_flow_factory
from flows.builtin.webserver.post import run_webserver
from tests.testcase import TestCase


class TestRunWebserver(TestCase):
    def setUp(self):
        self.post_job = self.set_up_patch(
            'flows.builtin.webserver.post.post_job'
        )
        self.expected_store = {'port': 8080}

    def test_run_webserver_posts_job(self):
        run_webserver()

        self.post_job.assert_called_once_with(
            simple_http_server_flow_factory,
            hierarchy=False,
            store=self.expected_store,
            capabilities={'port_is_free'}
        )

    def test_run_webserver_posts_job_with_specified_port(self):
        self.expected_store['port'] = 1234

        run_webserver(port=1234)

        self.post_job.assert_called_once_with(
            simple_http_server_flow_factory,
            hierarchy=False,
            store=self.expected_store,
            capabilities={'port_is_free'}
        )

    def test_run_webserver_composes_hierarchy(self):
        run_webserver(hierarchy=True)

        self.post_job.assert_called_once_with(
            simple_http_server_flow_factory,
            hierarchy=True,
            store=self.expected_store,
            capabilities={'port_is_free'}
        )
