from flows.builtin.webserver.tasks import SimpleHTTPServer
from tests.testcase import TestCase


class TestSimpleHTTPServerExecute(TestCase):
    def setUp(self):
        self.check_call = self.set_up_patch(
            'flows.builtin.webserver.tasks.check_call'
        )
        self.task = SimpleHTTPServer()

    def test_simple_http_server_runs_simple_http_server(self):
        self.task.execute(port=8432)

        expected_command = ['python', '-m', 'http.server', '8432']
        self.check_call.assert_called_once_with(expected_command)
