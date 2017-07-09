from flows.builtin.webserver.factory import simple_http_server_flow_factory
from jobrunner.utils import list_tasks_in_flow
from tests.testcase import TestCase


class TestSimpleHTTPServerFlowFactory(TestCase):
    def test_simple_http_server_flow_factory_creates_flow_with_name(self):
        flow = simple_http_server_flow_factory()

        self.assertEqual(flow.name, 'simple_http_server_flow')

    def test_simple_http_server_has_correct_tasks(self):
        flow = simple_http_server_flow_factory()

        expected_tasks = (
            'run_simple_webserver',
        )
        self.assertCountEqual(list_tasks_in_flow(flow), expected_tasks)

    def test_simple_http_server_is_retried(self):
        flow = simple_http_server_flow_factory()

        self.assertEqual(flow.retry._attempts, 10)
